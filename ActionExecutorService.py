using Kendo.Mvc.UI;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.Extensions.Logging;
using System.IO;
using System.Threading.Tasks;

namespace OnBoard.Apps.TagHelpers
{
    [HtmlTargetElement("ob-date-search")]
    public class CustomDateSearchTagHelper : TagHelper
    {
        private readonly ILogger<CustomDateSearchTagHelper> _logger;

        public CustomDateSearchTagHelper(ILogger<CustomDateSearchTagHelper> logger)
        {
            _logger = logger;
        }

        // Properties for configuration
        [HtmlAttributeName("field-name")]
        public string FieldName { get; set; } = "";

        [HtmlAttributeName("search-type")]
        public string SearchType { get; set; } = "equals";

        [HtmlAttributeName("orientation")]
        public string Orientation { get; set; } = "horizontal";

        [HtmlAttributeName("date-format")]
        public string DateFormat { get; set; } = "MM/dd/yyyy";

        private string ContainerStyle => Orientation == "horizontal" 
            ? "display: flex; gap: 10px; align-items: center;" 
            : "display: block; margin-bottom: 10px;";

        public override async Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
        {
            try
            {
                var writer = new StringWriter();
                var htmlHelper = GetHtmlHelper(context);

                // Render Kendo DropdownList
                var dropdown = htmlHelper.Kendo()
                    .DropDownList()
                    .Name("searchTypeDropdown")
                    .OptionLabel("Select Search Type")
                    .DataSource(ds => ds.Read(read => read.Action("", "")))
                    .BindTo(new[]
                    {
                        new { Text = "Equals", Value = "equals" },
                        new { Text = "Not Equals", Value = "not-equals" },
                        new { Text = "Greater Than", Value = "greater-than" },
                        new { Text = "Less Than", Value = "less-than" },
                        new { Text = "In Between", Value = "in-between" }
                    });

                dropdown.WriteTo(writer, System.Text.Encodings.Web.HtmlEncoder.Default);

                // Render Kendo DatePicker
                var datePickerSingle = htmlHelper.Kendo()
                    .DatePicker()
                    .Name("singleDate")
                    .Format(DateFormat)
                    .Placeholder("Enter Date");

                datePickerSingle.WriteTo(writer, System.Text.Encodings.Web.HtmlEncoder.Default);

                var datePickerFrom = htmlHelper.Kendo()
                    .DatePicker()
                    .Name("fromDate")
                    .Format(DateFormat)
                    .Placeholder("From Date");

                var datePickerTo = htmlHelper.Kendo()
                    .DatePicker()
                    .Name("toDate")
                    .Format(DateFormat)
                    .Placeholder("To Date");

                // Output Tag Helper content
                output.TagName = "div";
                output.Attributes.SetAttribute("style", ContainerStyle);

                output.Content.SetHtmlContent($@"
                    {writer}
                    {RenderIfInBetween(datePickerFrom, datePickerTo, SearchType)}
                    <input type='hidden' id='outputField' name='{FieldName}_output' value='' />
                    <script>
                        $(document).ready(function() {{
                            $('#searchTypeDropdown').on('change', function() {{
                                updateOutput();
                            }});

                            function updateOutput() {{
                                const searchType = $('#searchTypeDropdown').val();
                                let output = searchType;

                                $('#outputField').val(output);
                            }}
                        }});
                    </script>
                ");
            }
            catch (System.Exception ex)
            {
                _logger.LogError(ex, "Error in CustomDateSearchTagHelper: {Message}", ex.Message);
                output.Content.SetContent("Error rendering date search criteria.");
            }
        }

        private string RenderIfInBetween(IHtmlHelper htmlHelper, IHtmlHelper htmlHelperTo, string searchType)
        {
            if (searchType == "in-between")
            {
                var writerFrom = new StringWriter();
                var writerTo = new StringWriter();

                htmlHelper.WriteTo(writerFrom, System.Text.Encodings.Web.HtmlEncoder.Default);
                htmlHelperTo.WriteTo(writerTo, System.Text.Encodings.Web.HtmlEncoder.Default);

                return $"{writerFrom}{writerTo}";
            }
            return "";
        }

        private IHtmlHelper GetHtmlHelper(TagHelperContext context)
        {
            var httpContext = context.Items["HttpContext"] as Microsoft.AspNetCore.Http.HttpContext;
            var serviceProvider = httpContext?.RequestServices;
            return serviceProvider?.GetService(typeof(IHtmlHelper)) as IHtmlHelper;
        }
    }
}
