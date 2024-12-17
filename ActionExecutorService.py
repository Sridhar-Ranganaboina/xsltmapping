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

    <!-- DatePickers -->
    <div id="inBetweenDates" style="display: @(Model.SearchType == "in-between" ? "block" : "none");">
        <kendo-datepicker name="fromDate" style="width: 20%;" 
                          value="DateTime.Now" date-input="true">
        </kendo-datepicker>
        <kendo-datepicker name="toDate" style="width: 20%;" 
                          value="DateTime.Now" date-input="true">
        </kendo-datepicker>
    </div>

    <div id="singleDate" style="display: @(Model.SearchType != "in-between" ? "block" : "none");">
        <kendo-datepicker name="singleDate" style="width: 20%;" 
                          value="DateTime.Now" date-input="true">
        </kendo-datepicker>
    </div>

</div>

<script>
    $(document).ready(function () {
        // Bind to the dropdownlist change event
        $("#searchTypeDropdown").kendoDropDownList({
            change: function (e) {
                var selectedValue = this.value();

                if (selectedValue === "in-between") {
                    $("#inBetweenDates").show();
                    $("#singleDate").hide();
                } else {
                    $("#inBetweenDates").hide();
                    $("#singleDate").show();
                }
            }
        });
    });
</script>
