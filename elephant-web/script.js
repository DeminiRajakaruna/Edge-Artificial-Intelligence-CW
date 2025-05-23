const ESP32_URL = 'http://192.168.1.7'; // Change this to your ESP32's IP

function toggleBuzzer(state) {
  fetch(`${ESP32_URL}/buzzer/${state}`)
    .then(res => {
      if (res.ok) {
        document.getElementById('status').textContent = `Current Buzzer State: ${state.toUpperCase()}`;
      } else {
        alert('ESP32 did not respond');
      }
    })
    .catch(() => alert('Error: Could not reach ESP32'));
}
