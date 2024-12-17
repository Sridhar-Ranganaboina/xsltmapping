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
    <kendo-datepicker name="fromDate" id="fromDate" style="width: 20%;"
                      value="DateTime.Now" date-input="true"></kendo-datepicker>

    <kendo-datepicker name="toDate" id="toDate" style="width: 20%;"
                      value="DateTime.Now" date-input="true"></kendo-datepicker>

    <kendo-datepicker name="singleDate" id="singleDate" style="width: 20%;"
                      value="DateTime.Now" date-input="true"></kendo-datepicker>

</div>

<script>
    // Run when the DOM is fully loaded
    $(function () {
        const dropdown = $("#searchTypeDropdown").data("kendoDropDownList");

        // Bind change event
        dropdown.bind("change", function () {
            const selectedValue = this.value();

            if (selectedValue === "in-between") {
                // Show 'fromDate' and 'toDate'
                toggleDatePicker("#fromDate", true);
                toggleDatePicker("#toDate", true);
                toggleDatePicker("#singleDate", false);
            } else {
                // Show 'singleDate'
                toggleDatePicker("#singleDate", true);
                toggleDatePicker("#fromDate", false);
                toggleDatePicker("#toDate", false);
            }
        });

        // Function to toggle Kendo DatePickers
        function toggleDatePicker(selector, show) {
            const picker = $(selector).data("kendoDatePicker");
            if (picker) {
                picker.enable(show);
                $(selector).parent().toggle(show); // Hide/show the parent container
            }
        }

        // Initial state based on the current model value
        const initialValue = dropdown.value();
        if (initialValue === "in-between") {
            toggleDatePicker("#fromDate", true);
            toggleDatePicker("#toDate", true);
            toggleDatePicker("#singleDate", false);
        } else {
            toggleDatePicker("#singleDate", true);
            toggleDatePicker("#fromDate", false);
            toggleDatePicker("#toDate", false);
        }
    });
</script>
