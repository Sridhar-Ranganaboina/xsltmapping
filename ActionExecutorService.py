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

    <!-- Kendo DatePickers -->
    @if (Model.SearchType == "in-between")
    {
        <kendo-datepicker name="fromDate" id="fromDate" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>
        <kendo-datepicker name="toDate" id="toDate" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>
    }
    else
    {
        <kendo-datepicker name="singleDate" id="singleDate" style="width: 20%;"
                          value="DateTime.Now" date-input="true"></kendo-datepicker>
    }
</div>

<script>
    $(document).ready(function () {
        var dropdown = $("#searchTypeDropdown").data("kendoDropDownList");

        dropdown.bind("change", function () {
            var selectedValue = this.value();

            // Check which widgets to show/hide
            if (selectedValue === "in-between") {
                // Enable 'fromDate' and 'toDate' pickers
                enableDatePicker("#fromDate");
                enableDatePicker("#toDate");
                disableDatePicker("#singleDate");
            } else {
                // Enable 'singleDate' picker
                enableDatePicker("#singleDate");
                disableDatePicker("#fromDate");
                disableDatePicker("#toDate");
            }
        });

        function enableDatePicker(id) {
            var datePicker = $(id).data("kendoDatePicker");
            if (datePicker) {
                datePicker.enable(true);
                $(id).parent().show(); // Show it visually
            }
        }

        function disableDatePicker(id) {
            var datePicker = $(id).data("kendoDatePicker");
            if (datePicker) {
                datePicker.enable(false);
                $(id).parent().hide(); // Hide it visually
            }
        }
    });
</script>
