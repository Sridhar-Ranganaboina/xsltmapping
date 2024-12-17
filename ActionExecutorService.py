using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.AspNetCore.Mvc.ViewEngines;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using System.Threading.Tasks;

namespace SharedTagHelpers.TagHelpers
{
    [HtmlTargetElement("ob-date-search")]
    public class DateSearchTagHelper : TagHelper
    {
        private readonly ICompositeViewEngine _viewEngine;
        private readonly ILogger<DateSearchTagHelper> _logger;
        private readonly IHttpContextAccessor _httpContextAccessor;

        public DateSearchTagHelper(ICompositeViewEngine viewEngine, ILogger<DateSearchTagHelper> logger, IHttpContextAccessor httpContextAccessor)
        {
            _viewEngine = viewEngine;
            _logger = logger;
            _httpContextAccessor = httpContextAccessor;
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
                // Create a fake HttpContext to pass to the ViewContext
                var httpContext = _httpContextAccessor.HttpContext ?? new DefaultHttpContext();
                var actionContext = new ActionContext(httpContext, new Microsoft.AspNetCore.Routing.RouteData(), new Microsoft.AspNetCore.Mvc.Abstractions.ActionDescriptor());

                var viewContext = new ViewContext(
                    actionContext,
                    viewResult.View,
                    new ViewDataDictionary<object>(
                        new Microsoft.AspNetCore.Mvc.ModelBinding.EmptyModelMetadataProvider(),
                        new Microsoft.AspNetCore.Mvc.ModelBinding.ModelStateDictionary())
                    {
                        Model = model
                    },
                    sw
                );

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
