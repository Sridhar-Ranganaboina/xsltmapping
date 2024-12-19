string htmlContent = @"
<div style=""display:flex"">   
  <input id=""dropDownList"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace""></input>  
  <input id=""fromDateTxt"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace""></input>  
  <input id=""toDateTxt"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace""></input>
  <input id=""fromDatepicker"" value=""10/10/2011"" title=""datepicker"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace"" />
  <input id=""toDatePicker"" value=""10/10/2011"" title=""datepicker"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace"" />
  <input id=""singleDatePicker"" value=""10/10/2011"" title=""datepicker"" fill-mode=""FillMode.Outline"" rounded=""Rounded.Small"" style=""width:35%;background-color:ButtonFace"" />
</div>

<script>
    $(document).ready(function () {{
        $(\"#fromDateTxt\").kendoMaskedTextBox({{
            mask: \"00/0000\"
        }});
        $(\"#toDateTxt\").kendoMaskedTextBox({{
            mask: \"00/0000\"
        }});

        $(\"#fromDatepicker\").kendoDatePicker({{
            componentType: \"modern\"
        }});
        $(\"#toDatePicker\").kendoDatePicker({{
            componentType: \"modern\"
        }});

        $(\"#singleDatePicker\").kendoDatePicker({{
            componentType: \"modern\"
        }});

        $(\"#dropDownList\").kendoDropDownList({{
            dataSource: [\"equal\", \"in-between\"],
            value: \"modern\",
            change: function (e) {{
                var picker = $(\"#datepicker\").data(\"kendoDatePicker\");
                var type = this.value();
            }}
        }});
    }});
</script>";
