$('#copyright').text(new Date().getFullYear());

// scripts to display form in multiple stepss adapted from W3Schools https://www.w3schools.com/howto/howto_js_form_steps.asp

let currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(number) {
    // This function will display the specified tab of the form ...
    let tabs = document.getElementsByClassName("tab");
    tabs[number].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (number === 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (number === (tabs.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(number)
}

function nextPrev(number) {
    // This function will figure out which tab to display
    let tabs = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (number === 1 && !validateForm()) return false;
    // Hide the current tab:
    tabs[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + number;
    // if you have reached the end of the form... :
    if (currentTab >= tabs.length) {
        //...the form gets submitted:
        document.getElementById("profileCreationForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
        }
    }
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(number) {
    // This function removes the "active" class of all steps...   
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[number].className += " active";
}