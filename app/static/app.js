const form = document.getElementById("claim-form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const claim = {
        claim_amount: Number(document.getElementById("claim_amount").value),
        customer_age: Number(document.getElementById("customer_age").value),
        previous_claims: Number(document.getElementById("previous_claims").value),
        vehicle_age: Number(document.getElementById("vehicle_age").value),
        policy_age: Number(document.getElementById("policy_age").value)
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(claim)
        });

        if (!response.ok) {
            throw new Error("Prediction request failed");
        }

        const data = await response.json();

        document.getElementById("prediction").textContent =
            data.prediction;

        document.getElementById("fraud-probability").textContent =
            `${(data.fraud_probability * 100).toFixed(2)}%`;

        document.getElementById("not-fraud-probability").textContent =
            `${(data.not_fraud_probability * 100).toFixed(2)}%`;

        document.getElementById("result").classList.remove("hidden");

    } catch (error) {
        console.error(error);
        alert("Unable to get prediction from the server.");
    }
});
