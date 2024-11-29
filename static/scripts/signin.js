function signin() {
    cnic_input = document.getElementById("cnic");
    pass_input = document.getElementById("password");

    error_label = document.getElementById("error-label");
    error_label.style.color = "red";
    error_label.style.padding = "0px 0px 10px 0px";

    if (cnic_input.value && pass_input.value) {
        fetch("/api/auth/signin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                cnic: cnic_input.value,
                password: pass_input.value,
            }),
            credentials: "include",
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                if (jsonResponse.error === true) {
                    error_label.innerHTML = "One of the details was incorrect!";
                } else {
                    error_label.style.color = "green";
                    error_label.innerHTML = "Signin Successful";
                    setTimeout(function () {
                        window.location.replace("/");
                    }, 2000);
                }
            })
            .catch(function (error) {});
    } else {
        error_label.innerHTML = "Please fill all fields!";
    }
}
