#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lee un archivo embedded.mobileprovision y:
- Extrae el plist interno (CMS/DER -> XML plist) usando openssl
- Imprime metadatos relevantes del perfil
- Lista TODOS los UDIDs (ProvisionedDevices) y los guarda en un TXT
- Guarda el plist extraído para evidencia

Uso:
  python3 leer_mobileprovision.py embedded.mobileprovision

Requisitos:
  - Python 3.8+
  - OpenSSL disponible en PATH (openssl)
"""

import sys
import subprocess
import plistlib
from pathlib import Path
from datetime import datetime

def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "Error ejecutando comando:\n"
            f"Comando: {' '.join(cmd)}\n"
            f"STDERR:\n{p.stderr}\n"
            f"STDOUT:\n{p.stdout}\n"
        )
    return p.stdout

def extract_plist(input_path: Path, output_plist: Path) -> None:
    # embedded.mobileprovision es un CMS en DER.
    # Esto extrae el contenido (plist) sin intentar validar cadena (noverify).
    cmd = [
        "openssl", "cms",
        "-inform", "DER",
        "-verify",
        "-noverify",
        "-in", str(input_path),
        "-out", str(output_plist),
    ]
    run(cmd)

def safe_get(d: dict, key: str, default=None):
    return d.get(key, default)

def fmt_dt(x):
    if isinstance(x, datetime):
        return x.isoformat()
    return str(x) if x is not None else ""

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 leer_mobileprovision.py <ruta/embedded.mobileprovision>")
        sys.exit(2)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"No existe el archivo: {input_path}")
        sys.exit(2)

    out_plist = input_path.with_name("profile_extracted.plist")
    out_udids = input_path.with_name("udids_from_profile.txt")

    # 1) Extraer plist
    extract_plist(input_path, out_plist)

    # 2) Parsear plist
    profile = plistlib.loads(out_plist.read_bytes())

    # Metadatos comunes
    name = safe_get(profile, "Name")
    uuid = safe_get(profile, "UUID")
    team_name = safe_get(profile, "TeamName")
    team_ids = safe_get(profile, "TeamIdentifier", [])
    team_id = team_ids[0] if isinstance(team_ids, list) and team_ids else None
    creation = safe_get(profile, "CreationDate")
    expiration = safe_get(profile, "ExpirationDate")
    platform = safe_get(profile, "Platform", [])
    is_xcode_managed = safe_get(profile, "IsXcodeManaged")

    # Entitlements
    ent = safe_get(profile, "Entitlements", {}) or {}
    app_identifier = safe_get(ent, "application-identifier")
    get_task_allow = safe_get(ent, "get-task-allow")
    aps_env = safe_get(ent, "aps-environment")
    keychain_groups = safe_get(ent, "keychain-access-groups", [])
    beta_reports = safe_get(ent, "beta-reports-active")
    profile_type = "AdHoc/Distribution"
    # Heurística: si hay ProvisionedDevices suele ser AdHoc/Dev.
    # Si no hay, puede ser App Store/Enterprise (depende).
    # En AdHoc típicamente existe ProvisionedDevices.
    udids = safe_get(profile, "ProvisionedDevices", []) or []
    if udids:
        profile_type = "AdHoc (incluye ProvisionedDevices)"
    else:
        profile_type = "Sin ProvisionedDevices (posible App Store/Enterprise)"

    # Certificates (no imprimimos todo el contenido binario)
    dev_certs = safe_get(profile, "DeveloperCertificates", [])
    cert_count = len(dev_certs) if isinstance(dev_certs, list) else 0

    # 3) Listar UDIDs
    udids_sorted = sorted(udids)

    # 4) Salidas
    print("\nPerfil leído correctamente\n")
    print("Metadatos:")
    print(f"  Type: {profile_type}")
    print(f"  Name: {name}")
    print(f"  UUID: {uuid}")
    print(f"  TeamName: {team_name}")
    print(f"  TeamIdentifier: {team_id}")
    print(f"  CreationDate: {fmt_dt(creation)}")
    print(f"  ExpirationDate: {fmt_dt(expiration)}")
    print(f"  Platform: {platform}")
    print(f"  IsXcodeManaged: {is_xcode_managed}")
    print(f"  DeveloperCertificates (count): {cert_count}")

    print("\nEntitlements:")
    print(f"  application-identifier: {app_identifier}")
    print(f"  get-task-allow: {get_task_allow}")
    print(f"  aps-environment: {aps_env}")
    if keychain_groups:
        print(f"  keychain-access-groups: {keychain_groups}")
    if beta_reports is not None:
        print(f"  beta-reports-active: {beta_reports}")

    print("\nUDIDs (ProvisionedDevices):")
    print(f"  Total: {len(udids_sorted)}\n")
    for u in udids_sorted:
        print(u)

    # Guardar udids en archivo
    out_udids.write_text("\n".join(udids_sorted) + ("\n" if udids_sorted else ""), encoding="utf-8")

    print("\nArchivos generados:")
    print(f"  Plist extraído: {out_plist}")
    print(f"  Lista de UDIDs: {out_udids}")

if __name__ == "__main__":
    main()
