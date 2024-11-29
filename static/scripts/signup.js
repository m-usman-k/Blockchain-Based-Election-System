function signup() {
    name_input = document.getElementById("name");
    cnic_input = document.getElementById("cnic");
    pass_input = document.getElementById("password");

    error_label = document.getElementById("error-label");
    error_label.style.color = "red";
    error_label.style.padding = "0px 0px 10px 0px";

    if (name_input.value && cnic_input.value && pass_input.value) {
        fetch("/api/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name_input.value,
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
                    error_label.innerHTML = "CNIC already exists!";
                } else {
                    error_label.style.color = "green";
                    error_label.innerHTML = "Signup Successful";
                    setTimeout(function () {
                        window.location.replace("/signin");
                    }, 2000);
                }
            })
            .catch(function (error) {
                error_label.innerHTML = "Something went wrong!";
            });
    } else {
        error_label.innerHTML = "Please fill all fields!";
    }
}
