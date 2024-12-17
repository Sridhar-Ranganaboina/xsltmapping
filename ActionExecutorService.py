<Target Name="CopyViewsToOutput" AfterTargets="Build">
    <Copy 
      SourceFiles="Views/Shared/_DateSearchPartial.cshtml" 
      DestinationFolder="$(OutputPath)Views\Shared" 
      SkipUnchangedFiles="true" />
  </Target>
