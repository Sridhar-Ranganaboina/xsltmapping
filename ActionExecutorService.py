@model OnBoard.Apps.TagHelpers.Models.DateSearchModel
@addTagHelper *, Kendo.Mvc
@using Kendo.Mvc.UI

<div style="@(Model.Orientation == "horizontal" ? "display: flex; gap: 15px;" : "display: block;")">

    <!-- Kendo Dropdown -->
    <kendo-dropdownlist name="@Model.FieldName"
                        id="searchTypeDropdown"
                        value="@Model.SearchType">
        <datasource data="@Model.SearchTypes" />
    </kendo-dropdownlist>

    <!-- DatePickers for regular behavior -->
    <div id="datePickers" style="display: none;">
        <kendo-datepicker name="fromDate" id="fromDate" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>

        <kendo-datepicker name="toDate" id="toDate" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>
    </div>

    <!-- Masked TextBoxes for 'in-between' with specific formats -->
    <div id="maskedInputs" style="display: none;">
        <kendo-maskedtextbox name="fromMasked" id="fromMasked" style="width: 20%;"></kendo-maskedtextbox>
        <kendo-maskedtextbox name="toMasked" id="toMasked" style="width: 20%;"></kendo-maskedtextbox>
    </div>

    <!-- Single DatePicker -->
    <div id="singleDate" style="display: none;">
        <kendo-datepicker name="singleDate" id="singleDatePicker" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>
    </div>
</div>

<script>
    $(function () {
        const dropdown = $("#searchTypeDropdown").data("kendoDropDownList");

        // Function to set masks dynamically
        function setMaskedInputFormat(format) {
            const fromMasked = $("#fromMasked").data("kendoMaskedTextBox");
            const toMasked = $("#toMasked").data("kendoMaskedTextBox");

            if (format === "MM/YYYY") {
                fromMasked.setOptions({ mask: "00/0000", promptChar: "_" });
                toMasked.setOptions({ mask: "00/0000", promptChar: "_" });
            } else if (format === "YYYY") {
                fromMasked.setOptions({ mask: "0000", promptChar: "_" });
                toMasked.setOptions({ mask: "0000", promptChar: "_" });
            }
        }

        // Dropdown Change Event
        dropdown.bind("change", function () {
            const searchType = this.value();
            const dateFormat = "@Model.DateFormat";

            if (searchType === "in-between" && (dateFormat === "MM/YYYY" || dateFormat === "YYYY")) {
                $("#datePickers").hide();
                $("#singleDate").hide();
                $("#maskedInputs").show();

                // Apply masks
                setMaskedInputFormat(dateFormat);
            } else if (searchType === "in-between") {
                $("#maskedInputs").hide();
                $("#singleDate").hide();
                $("#datePickers").show();
            } else {
                $("#maskedInputs").hide();
                $("#datePickers").hide();
                $("#singleDate").show();
            }
        });

        // Initialize Kendo MaskedTextBoxes
        $("#fromMasked").kendoMaskedTextBox();
        $("#toMasked").kendoMaskedTextBox();

        // Trigger dropdown change to handle initial state
        dropdown.trigger("change");
    });
</script>
