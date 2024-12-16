
using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace OnBoard.Apps.TagHelpers
{
    [HtmlTargetElement("ob-date-search")]
    public class DateSearchTagHelper : TagHelper
    {
        private readonly ILogger<DateSearchTagHelper> _logger;

        public DateSearchTagHelper(ILogger<DateSearchTagHelper> logger)
        {
            _logger = logger;
        }

        [HtmlAttributeName("field-name")]
        public string? FieldName { get; set; }

        [HtmlAttributeName("search-type")]
        public string? SearchType { get; set; }

        [HtmlAttributeName("orientation")]
        public string Orientation { get; set; } = "horizontal";

        [HtmlAttributeName("date-format")]
        public string? DateFormat { get; set; }

        [HtmlAttributeName("output")]
        public string Output { get; private set; } = string.Empty;

        public override async Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
        {
            try
            {
                ValidateAttributes();

                string containerStyle = Orientation == "horizontal" 
                    ? "display: flex; gap: 15px; align-items: center;" 
                    : "display: block;";

                string dateInputHtml = GenerateDateInputHtml();
                string dropdownHtml = GenerateDropdownHtml();

                output.TagName = "div";
                output.Attributes.SetAttribute("class", "date-search-taghelper");
                output.Attributes.SetAttribute("style", containerStyle);
                output.Content.SetHtmlContent($"{dropdownHtml}<div id='datePickerContainer'>{dateInputHtml}</div>");

                output.PostContent.SetHtmlContent($@"
                    <script>
                        $(document).ready(function() {{
                            $('.k-datepicker').kendoDatePicker();

                            function enforcePattern(input, pattern) {{
                                input.on('input', function() {{
                                    const regex = new RegExp(pattern);
                                    if (!regex.test(this.value)) {{
                                        this.value = this.value.slice(0, -1);
                                    }}
                                }});
                            }}

                            enforcePattern($('#fromDate[placeholder="MM/YYYY"]'), '^\d{{0,2}}(\/\d{{0,4}})?$');
                            enforcePattern($('#toDate[placeholder="MM/YYYY"]'), '^\d{{0,2}}(\/\d{{0,4}})?$');

                            enforcePattern($('#fromDate[placeholder="YYYY"]'), '^\d{{0,4}}$');
                            enforcePattern($('#toDate[placeholder="YYYY"]'), '^\d{{0,4}}$');

                            $('#searchTypeDropdown, #fromDate, #toDate, #singleDate').on('change input', function() {{
                                updateOutput();
                            }});

                            function updateOutput() {{
                                const fieldName = '{FieldName ?? ""}';
                                const searchType = $('#searchTypeDropdown').val();
                                const singleDate = $('#singleDate').val();
                                const fromDate = $('#fromDate').val();
                                const toDate = $('#toDate').val();

                                let outputText = fieldName + searchType;

                                if (searchType === 'in-between') {{
                                    outputText += fromDate && toDate ? fromDate + '<>' + toDate : '';
                                }} else {{
                                    outputText += singleDate ? singleDate : '';
                                }}

                                $('#outputField').val(outputText);
                            }}
                        }});
                    </script>
                    <input type='hidden' id='outputField' name='{FieldName}_output' value='' />
                ");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing DateSearchTagHelper: {Message}", ex.Message);
                output.Content.SetContent("Error rendering date search criteria.");
            }

            await base.ProcessAsync(context, output);
        }

        private void ValidateAttributes()
        {
            var validSearchTypes = new HashSet<string> { "equals", "not-equals", "greater-than", "less-than", "in-between" };
            if (string.IsNullOrEmpty(SearchType) || !validSearchTypes.Contains(SearchType))
            {
                throw new ArgumentException("Invalid or missing SearchType.");
            }
        }

        private string GenerateDateInputHtml()
        {
            if (SearchType == "in-between")
            {
                return DateFormat switch
                {
                    "MM/DD/YYYY" => "<input class='k-datepicker' id='fromDate' name='fromDate' placeholder='From Date' />" +
                                     "<input class='k-datepicker' id='toDate' name='toDate' placeholder='To Date' />",
                    "MM/YYYY" => "<input class='k-textbox' id='fromDate' name='fromDate' placeholder='MM/YYYY' pattern='\d{2}/\d{4}' required />" +
                                  "<input class='k-textbox' id='toDate' name='toDate' placeholder='MM/YYYY' pattern='\d{2}/\d{4}' required />",
                    "YYYY" => "<input class='k-textbox' id='fromDate' name='fromDate' placeholder='YYYY' pattern='\d{4}' required />" +
                                "<input class='k-textbox' id='toDate' name='toDate' placeholder='YYYY' pattern='\d{4}' required />",
                    _ => ""
                };
            }
            else
            {
                return "<input class='k-datepicker' id='singleDate' name='singleDate' placeholder='Enter Date' />";
            }
        }

        private string GenerateDropdownHtml()
        {
            return "<select id='searchTypeDropdown' name='searchType'>" +
                   "<option value='equals'" + (SearchType == "equals" ? " selected" : "") + ">Equals</option>" +
                   "<option value='not-equals'" + (SearchType == "not-equals" ? " selected" : "") + ">Not Equal To</option>" +
                   "<option value='greater-than'" + (SearchType == "greater-than" ? " selected" : "") + ">Greater Than</option>" +
                   "<option value='less-than'" + (SearchType == "less-than" ? " selected" : "") + ">Less Than</option>" +
                   "<option value='in-between'" + (SearchType == "in-between" ? " selected" : "") + ">In Between</option>" +
                   "</select>";
        }
    }
}
