function fetchCandidates() {
    let cnic = getCookie("cnic");
    let password = getCookie("password");

    let data = {
        cnic: cnic,
        password: password,
    };
    fetch("/api/vote/get-candidates", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((candidates) => {
            displayCandidates(candidates);
        })
        .catch((error) => {
            window.location.replace("/logout");
        });
}

function getCookie(name) {
    let match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? match[2] : null;
}

function displayCandidates(candidates) {
    const cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "";

    candidates.forEach((candidate) => {
        const card = document.createElement("div");
        card.classList.add("candidate-card");

        const img = document.createElement("img");
        img.src =
            `/static/images/${candidate.image}` ||
            "https://via.placeholder.com/150";
        img.alt = candidate.name;
        img.classList.add("candidate-img");

        const name = document.createElement("h2");
        name.textContent = candidate.name;

        const party = document.createElement("p");
        party.classList.add("party");
        party.textContent = `Party: ${candidate.party}`;

        const pollId = document.createElement("p");
        pollId.classList.add("poll-id");
        pollId.textContent = `Poll ID: ${candidate.poll_id}`;

        const voteButton = document.createElement("button");
        voteButton.classList.add("vote-btn");
        voteButton.textContent = "Vote";
        voteButton.addEventListener("click", () => postVote(candidate));

        card.appendChild(img);
        card.appendChild(name);
        card.appendChild(party);
        card.appendChild(pollId);
        card.appendChild(voteButton);

        cardContainer.appendChild(card);
    });
}

function postVote(candidate) {
    const cnic = getCookie("cnic");
    const password = getCookie("password");

    const data = {
        cnic: cnic,
        password: password,
        poll_id: candidate.poll_id, // Assuming poll_id is used to identify the candidate
    };

    fetch("/api/vote/post-vote", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((result) => {
            if (!result.error) {
                showPopup("Vote successfully added!", true);
                disableAllVoteButtons();
            } else {
                showPopup("Vote not successful. Please try again.", false);
            }
        })
        .catch((error) => {
            showPopup("An error occurred. Please try again later.", false);
        });
}

function disableAllVoteButtons() {
    const buttons = document.querySelectorAll(".vote-btn");
    buttons.forEach((button) => {
        button.disabled = true;
        button.classList.add("disabled");
    });
}

function showPopup(message, success) {
    const popup = document.createElement("div");
    popup.classList.add("popup", success ? "success" : "error");

    const popupMessage = document.createElement("p");
    popupMessage.textContent = message;

    const closeButton = document.createElement("button");
    closeButton.textContent = "Close";
    closeButton.classList.add("close-btn");
    closeButton.addEventListener("click", () => {
        popup.remove();
    });

    popup.appendChild(popupMessage);
    if (!success) {
        popup.appendChild(closeButton);
    }

    document.body.appendChild(popup);

    if (success) {
        window.location.replace("/vote-details");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    fetchCandidates();
});
