using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.AspNetCore.Mvc.ViewEngines;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;

namespace SharedTagHelpers.TagHelpers
{
    [HtmlTargetElement("ob-date-search")]
    public class DateSearchTagHelper : TagHelper
    {
        private readonly ICompositeViewEngine _viewEngine;
        private readonly ILogger<DateSearchTagHelper> _logger;

        public DateSearchTagHelper(ICompositeViewEngine viewEngine, ILogger<DateSearchTagHelper> logger)
        {
            _viewEngine = viewEngine;
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

        public override async Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
        {
            output.TagName = "div";
            output.Attributes.SetAttribute("class", "date-search-container");

            var model = new
            {
                FieldName,
                SearchType,
                Orientation,
                DateFormat
            };

            // Render the partial view dynamically
            var partialContent = await RenderPartialViewAsync("_DateSearchPartial", model);
            output.Content.SetHtmlContent(partialContent);
        }

        private async Task<string> RenderPartialViewAsync(string viewName, object model)
        {
            using var sw = new System.IO.StringWriter();
            var viewResult = _viewEngine.FindView(null, viewName, false);

            if (viewResult.Success)
            {
                var viewContext = new ViewContext
                {
                    Writer = sw,
                    ViewData = new Microsoft.AspNetCore.Mvc.ViewFeatures.ViewDataDictionary<object>(
                        new Microsoft.AspNetCore.Mvc.ModelBinding.EmptyModelMetadataProvider(),
                        new Microsoft.AspNetCore.Mvc.ModelBinding.ModelStateDictionary())
                    {
                        Model = model
                    }
                };
                await viewResult.View.RenderAsync(viewContext);
            }
            else
            {
                _logger.LogError($"View {viewName} not found.");
                sw.Write($"<div>Error: View {viewName} not found.</div>");
            }

            return sw.ToString();
        }
    }
}
