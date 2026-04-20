document.getElementById('algorithm').addEventListener('change', function() {
    const shiftContainer = document.getElementById('shiftContainer');
    if (this.value === 'caesar') {
        shiftContainer.style.display = 'block';
    } else {
        shiftContainer.style.display = 'none';
    }
});

async function processData(action) {
    const text = document.getElementById('inputText').value.trim();
    const algorithm = document.getElementById('algorithm').value;
    const shiftValue = parseInt(document.getElementById('shiftValue').value) || 3;
    const errorMsg = document.getElementById('errorMsg');
    const outputText = document.getElementById('outputText');

    errorMsg.textContent = "";
    outputText.value = "";

    // Basic Validation
    if (!text) {
        errorMsg.textContent = "Please enter some text.";
        return;
    }
    if (!algorithm) {
        errorMsg.textContent = "Please select an algorithm.";
        return;
    }
    if (action === 'decrypt' && algorithm === 'sha256') {
        errorMsg.textContent = "SHA-256 is a one-way hash. It cannot be decrypted.";
        return;
    }

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                text: text, 
                algorithm: algorithm, 
                action: action,
                shift: shiftValue
            })
        });

        const data = await response.json();

        if (response.ok) {
            outputText.value = data.result;
        } else {
            errorMsg.textContent = data.error || "An error occurred.";
        }
    } catch (error) {
        errorMsg.textContent = "Failed to connect to the server.";
    }
}

function copyToClipboard() {
    const outputText = document.getElementById('outputText');
    if (!outputText.value) {
        document.getElementById('errorMsg').textContent = "Nothing to copy!";
        return;
    }

    outputText.select();
    document.execCommand('copy');
    
    const copyBtn = document.querySelector('.copy');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Copied! ✔";
    copyBtn.style.backgroundColor = "#10B981"; 
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.backgroundColor = ""; 
    }, 2000);
}