// index.js

function parseTransitions(text) {
  const lines = text.split('\n').map(line => line.trim()).filter(Boolean);
  const transitions = lines.map(line => {
    const [fromPart, toPart] = line.split(':');
    const from = fromPart.replace(/[()]/g, '').split(',');
    const to = toPart.replace(/[()]/g, '').split(',');
    return { from, to };
  });
  return transitions;
}

document.getElementById("apd-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const transitionsText = document.getElementById("transitions").value;
  const transitions = parseTransitions(transitionsText);

  const initialState = document.getElementById("initial-state").value;
  const acceptanceType = document.getElementById("acceptance-type").value;
  const finalState = document.getElementById("final-state").value;
  const inputWord = document.getElementById("input-word").value;

  const payload = {
    transitions: transitions,
    initial_state: initialState,
    acceptance_type: acceptanceType,
    final_state: finalState,
    input_word: inputWord
  };

  try {
    const response = await fetch("/simulate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });


    const result = await response.json();
    document.getElementById("result").textContent =
      result.accepted ? "Palabra ACEPTADA por el lenguaje." : "Palabra NO aceptada.";
  } catch (error) {
    document.getElementById("result").textContent = "Error al procesar la solicitud.";
    console.error(error);
  }
});
