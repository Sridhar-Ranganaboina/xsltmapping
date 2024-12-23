using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.ViewEngines;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Razor.TagHelpers;
using Moq;
using Xunit;

namespace OnBoard.Apps.TagHelpers.Tests
{
    public class DateSearchTagHelperTests
    {
        private readonly Mock<ICompositeViewEngine> _viewEngineMock;
        private readonly Mock<IHttpContextAccessor> _httpContextAccessorMock;
        private readonly Mock<ITempDataProvider> _tempDataProviderMock;
        private readonly DateSearchTagHelper _tagHelper;

        public DateSearchTagHelperTests()
        {
            _viewEngineMock = new Mock<ICompositeViewEngine>();
            _httpContextAccessorMock = new Mock<IHttpContextAccessor>();
            _tempDataProviderMock = new Mock<ITempDataProvider>();

            _tagHelper = new DateSearchTagHelper(_viewEngineMock.Object, _httpContextAccessorMock.Object, _tempDataProviderMock.Object);
        }

        [Fact]
        public async Task ProcessAsync_SetsTagNameAndClass()
        {
            // Arrange
            var context = new TagHelperContext(
                new TagHelperAttributeList(),
                new TagHelperContextItems(),
                Guid.NewGuid().ToString("N"));

            var output = new TagHelperOutput(
                "ob-date-search",
                new TagHelperAttributeList(),
                (useCachedResult, encoder) =>
                    Task.FromResult<TagHelperContent>(new DefaultTagHelperContent()));

            _viewEngineMock
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.NotFound("_DateLookupPartial", new[] { "_DateLookupPartial" }));

            // Act
            await _tagHelper.ProcessAsync(context, output);

            // Assert
            Assert.Equal("div", output.TagName);
            Assert.Contains(output.Attributes, a => a.Name == "class" && a.Value.ToString() == "date-search-container");
        }

        [Fact]
        public async Task ProcessAsync_RendersHiddenFieldWhenAspForIsSet()
        {
            // Arrange
            var modelExplorer = new EmptyModelMetadataProvider().GetModelExplorerForType(typeof(string), "TestValue");
            var modelExpression = new ModelExpression("TestField", modelExplorer);

            _tagHelper.For = modelExpression;
            _tagHelper.FieldName = "TestField";

            var context = new TagHelperContext(
                new TagHelperAttributeList(),
                new TagHelperContextItems(),
                Guid.NewGuid().ToString("N"));

            var output = new TagHelperOutput(
                "ob-date-search",
                new TagHelperAttributeList(),
                (useCachedResult, encoder) =>
                    Task.FromResult<TagHelperContent>(new DefaultTagHelperContent()));

            _viewEngineMock
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.NotFound("_DateLookupPartial", new[] { "_DateLookupPartial" }));

            // Act
            await _tagHelper.ProcessAsync(context, output);

            // Assert
            var content = output.Content.GetContent();
            Assert.Contains("<input", content);
            Assert.Contains("type=\"hidden\"", content);
            Assert.Contains("name=\"TestField\"", content);
            Assert.Contains("value=\"TestValue\"", content);
        }

        [Fact]
        public async Task RenderPartialViewAsync_ReturnsErrorWhenViewNotFound()
        {
            // Arrange
            _httpContextAccessorMock.Setup(h => h.HttpContext).Returns(new DefaultHttpContext());

            _viewEngineMock
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.NotFound("_DateLookupPartial", new[] { "_DateLookupPartial" }));

            // Act
            var result = await _tagHelper.RenderPartialViewAsync("_DateLookupPartial", new object());

            // Assert
            Assert.Contains("Error: View _DateLookupPartial not found.", result);
        }

        [Fact]
        public async Task RenderPartialViewAsync_RendersViewSuccessfully()
        {
            // Arrange
            var mockView = new Mock<IView>();
            var stringWriter = new StringWriter();
            mockView
                .Setup(v => v.RenderAsync(It.IsAny<ViewContext>()))
                .Callback<ViewContext>(vc => vc.Writer.Write("Rendered Content"))
                .Returns(Task.CompletedTask);

            _httpContextAccessorMock.Setup(h => h.HttpContext).Returns(new DefaultHttpContext());

            _viewEngineMock
                .Setup(ve => ve.FindView(It.IsAny<ActionContext>(), "_DateLookupPartial", false))
                .Returns(ViewEngineResult.Found("_DateLookupPartial", mockView.Object));

            // Act
            var result = await _tagHelper.RenderPartialViewAsync("_DateLookupPartial", new object());

            // Assert
            Assert.Equal("Rendered Content", result);
        }
    }
}
