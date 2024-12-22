using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.ViewEngines;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.Extensions.Logging;
using Moq;
using System.IO;
using System.Threading.Tasks;
using Xunit;

namespace OnBoard.Apps.TagHelpers.UnitTests
{
    public class DateSearchTagHelperTests
    {
        private readonly Mock<ICompositeViewEngine> _mockViewEngine;
        private readonly Mock<ILogger<DateSearchTagHelper>> _mockLogger;
        private readonly Mock<IHttpContextAccessor> _mockHttpContextAccessor;
        private readonly Mock<ITempDataProvider> _mockTempDataProvider;

        public DateSearchTagHelperTests()
        {
            _mockViewEngine = new Mock<ICompositeViewEngine>();
            _mockLogger = new Mock<ILogger<DateSearchTagHelper>>();
            _mockHttpContextAccessor = new Mock<IHttpContextAccessor>();
            _mockTempDataProvider = new Mock<ITempDataProvider>();
        }

        [Fact]
        public async Task ProcessAsync_RendersPartialView_WhenViewExists()
        {
            // Arrange
            var tagHelper = new DateSearchTagHelper(
                _mockViewEngine.Object,
                _mockLogger.Object,
                _mockHttpContextAccessor.Object,
                _mockTempDataProvider.Object
            )
            {
                FieldName = "TestField",
                SearchType = "Contains",
                DateFormat = "MM/dd/yyyy",
                Orientation = "vertical"
            };

            var mockView = new Mock<IView>();
            _mockViewEngine
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.Found("_DateLookupPartial", mockView.Object));

            var tagHelperContext = new TagHelperContext(
                new TagHelperAttributeList(),
                new Dictionary<object, object>(),
                "test"
            );

            var tagHelperOutput = new TagHelperOutput(
                "ob-date-search",
                new TagHelperAttributeList(),
                (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(new DefaultTagHelperContent())
            );

            var stringWriter = new StringWriter();
            mockView
                .Setup(v => v.RenderAsync(It.IsAny<ViewContext>()))
                .Callback<ViewContext>(vc =>
                {
                    stringWriter.Write("<div>Rendered View</div>");
                })
                .Returns(Task.CompletedTask);

            _mockHttpContextAccessor.Setup(hca => hca.HttpContext).Returns(new DefaultHttpContext());

            // Act
            await tagHelper.ProcessAsync(tagHelperContext, tagHelperOutput);

            // Assert
            Assert.Equal("div", tagHelperOutput.TagName);
            Assert.Contains("date-search-container", tagHelperOutput.Attributes["class"].Value.ToString());
            Assert.Contains("Rendered View", tagHelperOutput.Content.GetContent());
        }

        [Fact]
        public async Task ProcessAsync_ReturnsErrorMessage_WhenViewDoesNotExist()
        {
            // Arrange
            var tagHelper = new DateSearchTagHelper(
                _mockViewEngine.Object,
                _mockLogger.Object,
                _mockHttpContextAccessor.Object,
                _mockTempDataProvider.Object
            );

            _mockViewEngine
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.NotFound("_DateLookupPartial", new[] { "TestLocation" }));

            var tagHelperContext = new TagHelperContext(
                new TagHelperAttributeList(),
                new Dictionary<object, object>(),
                "test"
            );

            var tagHelperOutput = new TagHelperOutput(
                "ob-date-search",
                new TagHelperAttributeList(),
                (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(new DefaultTagHelperContent())
            );

            _mockHttpContextAccessor.Setup(hca => hca.HttpContext).Returns(new DefaultHttpContext());

            // Act
            await tagHelper.ProcessAsync(tagHelperContext, tagHelperOutput);

            // Assert
            Assert.Equal("div", tagHelperOutput.TagName);
            Assert.Contains("Error: View _DateLookupPartial not found.", tagHelperOutput.Content.GetContent());
            _mockLogger.Verify(
                logger => logger.LogError(It.Is<string>(s => s.Contains("_DateLookupPartial not found"))),
                Times.Once
            );
        }

        [Fact]
        public void Constructor_InitializesCorrectly()
        {
            // Arrange & Act
            var tagHelper = new DateSearchTagHelper(
                _mockViewEngine.Object,
                _mockLogger.Object,
                _mockHttpContextAccessor.Object,
                _mockTempDataProvider.Object
            );

            // Assert
            Assert.NotNull(tagHelper);
        }
    }
}
