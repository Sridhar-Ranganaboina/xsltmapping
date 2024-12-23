[Fact]
public async Task ProcessAsync_AddsHiddenField_WhenForIsNotNull()
{
    // Arrange
    var tagHelper = new DateSearchTagHelper(
        _mockViewEngine.Object,
        _mockHttpContextAccessor.Object,
        _mockTempDataProvider.Object
    )
    {
        FieldName = "TestField",
        SearchType = "Contains",
        DateFormat = "MM/dd/yyyy",
        Orientation = "vertical",
        For = new ModelExpression("TestProperty", 
            new ViewDataDictionary(new Microsoft.AspNetCore.Mvc.ModelBinding.EmptyModelMetadataProvider(), 
            new Microsoft.AspNetCore.Mvc.ModelBinding.ModelStateDictionary())
            {
                Model = "TestValue"
            })
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
    Assert.Contains("<input", tagHelperOutput.Content.GetContent());
    Assert.Contains("type=\"hidden\"", tagHelperOutput.Content.GetContent());
    Assert.Contains("name=\"TestProperty\"", tagHelperOutput.Content.GetContent());
    Assert.Contains("value=\"TestValue\"", tagHelperOutput.Content.GetContent());
    Assert.Contains($"id=\"{tagHelper.FieldName}\"", tagHelperOutput.Content.GetContent());
}
