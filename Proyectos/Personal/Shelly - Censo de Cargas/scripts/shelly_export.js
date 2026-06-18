let SERVER_URL = "http://192.168.3.95:8765/shelly";
let EM_ID = 0;
let PERIOD_MS = 60000;
let sending = false;

function log(msg) {
  print("[energy-export] " + msg);
}

function postReading(payload) {
  Shelly.call(
    "HTTP.POST",
    {
      url: SERVER_URL,
      body: JSON.stringify(payload),
      content_type: "application/json",
      timeout: 10
    },
    function (res, err_code, err_msg) {
      if (err_code !== 0) {
        log("HTTP.POST error: " + err_code + " / " + err_msg);
      } else {
        log("POST ok");
      }
      sending = false;
    }
  );
}

function collectAndSend() {
  if (sending) {
    log("skip: previous send still running");
    return;
  }

  sending = true;

  Shelly.call("EM.GetStatus", { id: EM_ID }, function (res, err_code, err_msg) {
    if (err_code !== 0 || !res) {
      log("EM.GetStatus error: " + err_code + " / " + err_msg);
      sending = false;
      return;
    }

    let payload = {
      source: "shelly_pro_3em",
      em_id: EM_ID,
      sent_at_unix: Math.floor(Date.now() / 1000),
      reading: {
        ...res,
        a_total: res.a_total_act_energy || res.a_act_energy?.total || 0,
        b_total: res.b_total_act_energy || res.b_act_energy?.total || 0,
        c_total: res.c_total_act_energy || res.c_act_energy?.total || 0,
        total: res.total_act_energy || res.total_act? res.total_act : 0
      }
    };

    postReading(payload);
  });
}

Timer.set(5000, false, collectAndSend);
Timer.set(PERIOD_MS, true, collectAndSend);

log("script started");
