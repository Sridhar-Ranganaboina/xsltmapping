public class EmbeddedResourceViewLocationExpander : IViewLocationExpander
{
    public IEnumerable<string> ExpandViewLocations(ViewLocationExpanderContext context, IEnumerable<string> viewLocations)
    {
        // Assuming the namespace of your class library is "MyClassLibrary"
        yield return "~/EmbeddedResources/MyClassLibrary/Views/{1}/{0}.cshtml";
        yield return "~/EmbeddedResources/MyClassLibrary/Views/Shared/{0}.cshtml";
    }

    public void PopulateValues(ViewLocationExpanderContext context)
    {
        // No additional values to populate
    }
}
