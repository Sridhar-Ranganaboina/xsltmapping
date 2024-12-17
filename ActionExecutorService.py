@model dynamic

<div style="@(Model.Orientation == "horizontal" ? "display: flex; gap: 15px;" : "display: block;")">
    <kendo-dropdownlist id="searchTypeDropdown" name="searchType" value="@Model.SearchType">
        <option value="equals">Equals</option>
        <option value="not-equals">Not Equal To</option>
        <option value="greater-than">Greater Than</option>
        <option value="less-than">Less Than</option>
        <option value="in-between">In Between</option>
    </kendo-dropdownlist>

    @if (Model.SearchType == "in-between")
    {
        <kendo-datepicker id="fromDate" name="fromDate" placeholder="From Date"></kendo-datepicker>
        <kendo-datepicker id="toDate" name="toDate" placeholder="To Date"></kendo-datepicker>
    }
    else
    {
        <kendo-datepicker id="singleDate" name="singleDate" placeholder="Enter Date"></kendo-datepicker>
    }
</div>
