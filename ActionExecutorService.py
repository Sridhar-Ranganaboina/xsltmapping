<style>
    /* Standardize height and line-height for Kendo components */
    .k-input,
    .k-dropdownlist,
    .k-datepicker .k-input,
    .k-maskedtextbox .k-input {
        height: 32px !important; /* Set your desired height */
        line-height: 32px !important; /* Align text vertically */
        font-size: 14px; /* Optional: Ensure consistent font size */
        box-sizing: border-box; /* Maintain padding within the height */
    }

    /* Add some padding for better spacing */
    .k-input {
        padding: 4px 8px;
    }

    /* Target the MaskedTextBox specifically */
    .k-maskedtextbox {
        height: 32px !important;
        line-height: 32px !important;
    }

    /* Target the DropdownList specifically */
    .k-dropdownlist {
        height: 32px !important;
    }

    /* Target the DatePicker specifically */
    .k-datepicker {
        height: 32px !important;
    }

    /* Optional: Ensure placeholder alignment for consistency */
    .k-placeholder {
        line-height: 32px !important;
    }
</style>
