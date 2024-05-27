function generateItemInputs() {
    const numItems = document.getElementById('num_items').value;
    const itemsInputs = document.getElementById('items_inputs');
    itemsInputs.innerHTML = '';

    for (let i = 0; i < numItems; i++) {
        const itemDiv = document.createElement('div');
        itemDiv.innerHTML = `
            <label for="value_${i}">Valor del ítem ${i + 1}:</label>
            <input type="number" id="value_${i}" min="1">
            <label for="weight_${i}">Peso del ítem ${i + 1}:</label>
            <input type="number" id="weight_${i}" min="1">
        `;
        itemsInputs.appendChild(itemDiv);
    }
}

async function calculateKnapsack() {
    const numItems = document.getElementById('num_items').value;
    const items = [];
    for (let i = 0; i < numItems; i++) {
        const value = document.getElementById(`value_${i}`).value;
        const weight = document.getElementById(`weight_${i}`).value;
        items.push({ value: parseInt(value), weight: parseInt(weight) });
    }
    const maxWeight = parseInt(document.getElementById('max_weight').value);
    const response = await fetch('/knapsack', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ items: items, max_weight: maxWeight })
    });
    const result = await response.json();
    document.getElementById('result').innerText = `Mejor combinación de ítems: ${JSON.stringify(result.selected_items)}\nValor total: ${result.value}`;
    const img = document.getElementById('evolution_plot');
    img.src = `data:image/png;base64,${result.plot_url}`;
    img.style.display = 'block';
}
