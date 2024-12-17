function updateHiddenField() {
    var fieldName = $("#FieldName").val(); // Assuming dropdown id = FieldName
    var searchType = $("#SearchType").val(); // Assuming dropdown id = SearchType
    var singleDate = $("#singleDate").val(); // Single datepicker value
    var fromDate = $("#fromDate").val(); // "From Date" value
    var toDate = $("#toDate").val(); // "To Date" value

    // Concatenate the values
    var hiddenFieldValue = fieldName + "_" + searchType + "_" + singleDate + "_" + fromDate + "_" + toDate;

    // Update the hidden field
    $("#hiddenField").val(hiddenFieldValue);
}
