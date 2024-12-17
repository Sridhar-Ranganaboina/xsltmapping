public class CustomViewLocationExpander : IViewLocationExpander
{
    public IEnumerable<string> ExpandViewLocations(ViewLocationExpanderContext context, IEnumerable<string> viewLocations)
    {
        // Add the existing view locations
        foreach (var location in viewLocations)
        {
            yield return location;
        }

        // Add the location for embedded resources
        yield return "~/EmbeddedResources/OnBoard.Apps.TagHelpers/Views/{1}/{0}.cshtml";
        yield return "~/EmbeddedResources/OnBoard.Apps.TagHelpers/Views/Shared/{0}.cshtml";
    }

    public void PopulateValues(ViewLocationExpanderContext context)
    {
        // No additional values to populate
    }
}
