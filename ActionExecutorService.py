using Microsoft.AspNetCore.Razor.TagHelpers;
using System;
using System.Collections.Generic;

namespace OnBoard.Apps.TagHelpers
{
    public enum SearchTypeEnum { Equals, NotEquals, GreaterThan, LessThan, InBetween }
    public enum DateFormatEnum { MMDDYYYY, MMYYYY, YYYY }

    [HtmlTargetElement("ob-date-search")]
    public class DateSearchTagHelper : TagHelper
    {
        [HtmlAttributeName("field-name")]
        public string? FieldName { get; set; }

        [HtmlAttributeName("search-type")]
        public SearchTypeEnum SearchType { get; set; }

        [HtmlAttributeName("orientation")]
        public string Orientation { get; set; } = "horizontal";

        [HtmlAttributeName("date-format")]
        public DateFormatEnum DateFormat { get; set; }

        public override void Process(TagHelperContext context, TagHelperOutput output)
        {
            output.TagName = "div";
            output.Attributes.SetAttribute("class", "date-search-container");
            output.Content.SetHtmlContent($@"<div style='{{(Orientation == 'horizontal' ? 'display: flex; gap: 15px;' : 'display: block;')}}'>
                <div style='width: 40%;'>
                    <kendo-dropdownlist name='{FieldName}' id='search_type_{FieldName}' value='{SearchType}' class='update_hidden'>
                        <datasource data='@Enum.GetNames(typeof(SearchTypeEnum))' />
                    </kendo-dropdownlist>
                </div>
                <div id='date_pickers_div_{FieldName}' style='display: none; width:50%;'>
                    <kendo-datepicker name='fromDate' id='from_datepicker_{FieldName}' style='width: 25%;' date-input='true' class='update_hidden'></kendo-datepicker>
                    <kendo-datepicker name='toDate' id='to_datepicker_{FieldName}' style='width: 25%;' date-input='true' class='update_hidden'></kendo-datepicker>
                </div>
                <div id='masked_inputs_div_{FieldName}' style='display: none;width:50%;'>
                    <kendo-maskedtextbox name='fromMasked' id='from_masked_txt_{FieldName}' style='width: 25%;' placeholder='{DateFormat}' class='update_hidden'></kendo-maskedtextbox>
                    <kendo-maskedtextbox name='toMasked' id='to_masked_txt_{FieldName}' style='width: 25%;' placeholder='{DateFormat}' class='update_hidden'></kendo-maskedtextbox>
                </div>
                <div id='single_date_div_{FieldName}' style='display: none;width:50%;'>
                    <kendo-datepicker name='singleDate' id='single_datepicker_{FieldName}' style='width: 50%;' date-input='true' class='update_hidden'></kendo-datepicker>
                </div>
                <input type='hidden' id='hidden_{FieldName}' value='' />
            </div>
            <script>
                $(function () {
                    const searchTypeDropdownId = '#search_type_{FieldName}';
                    const fromMaskedTxtId = '#from_masked_txt_{FieldName}';
                    const toMaskedTxtId = '#to_masked_txt_{FieldName}';
                    const fromDatepickerId = '#from_datepicker_{FieldName}';
                    const toDatepickerId = '#to_datepicker_{FieldName}';
                    const singleDatepickerId = '#single_datepicker_{FieldName}';
                    const datePickersDivId = '#date_pickers_div_{FieldName}';
                    const maskedInputsDivId = '#masked_inputs_div_{FieldName}';
                    const singleDateDivId = '#single_date_div_{FieldName}';

                    function setMaskedInputFormat(format) {
                        const fromMasked = $(fromMaskedTxtId).data('kendoMaskedTextBox');
                        const toMasked = $(toMaskedTxtId).data('kendoMaskedTextBox');

                        if (format === 'MMYYYY') {
                            fromMasked.setOptions({ mask: '00/0000', promptChar: '_' });
                            toMasked.setOptions({ mask: '00/0000', promptChar: '_' });
                        } else if (format === 'YYYY') {
                            fromMasked.setOptions({ mask: '0000', promptChar: '_' });
                            toMasked.setOptions({ mask: '0000', promptChar: '_' });
                        }
                    }

                    function updateHiddenField() {
                        const searchType = $(searchTypeDropdownId).val();
                        const fieldName = '{FieldName}';
                        const dateFormat = '{DateFormat}';
                        const singleDate = new Date($(singleDatepickerId).val());
                        const fromDate = new Date($(fromDatepickerId).val());
                        const toDate = new Date($(toDatepickerId).val());
                        const fromMaskedText = new Date($(fromMaskedTxtId).val());
                        const toMaskedText = new Date($(toMaskedTxtId).val());

                        let hiddenFieldValue = '';
                        if (searchType === 'InBetween' && dateFormat === 'MMDDYYYY') {
                            hiddenFieldValue = `{field_name:${fieldName},search_type:${searchType},single_date:'',from_date:${isNaN(fromDate) ? '' : fromDate.toISOString().split('T')[0]},to_date:${isNaN(toDate) ? '' : toDate.toISOString().split('T')[0]}}`;
                        } else if (searchType === 'InBetween' && dateFormat !== 'MMDDYYYY') {
                            hiddenFieldValue = `{field_name:${fieldName},search_type:${searchType},single_date:'',from_date:${isNaN(fromMaskedText) ? '' : fromMaskedText.toISOString().split('T')[0]},to_date:${isNaN(toMaskedText) ? '' : toMaskedText.toISOString().split('T')[0]}}`;
                        } else {
                            hiddenFieldValue = `{field_name:${fieldName},search_type:${searchType},single_date:${isNaN(singleDate) ? '' : singleDate.toISOString().split('T')[0]},from_date:'',to_date:''}`;
                        }
                        $('#hidden_{FieldName}').val(hiddenFieldValue);
                    }

                    const dropdown = $(searchTypeDropdownId).data('kendoDropDownList');
                    dropdown.bind('change', function () {
                        const searchType = this.value();
                        if (searchType === 'InBetween' && (dateFormat === 'MMYYYY' || dateFormat === 'YYYY')) {
                            $(datePickersDivId).hide();
                            $(singleDateDivId).hide();
                            $(maskedInputsDivId).show();
                            setMaskedInputFormat(dateFormat);
                        } else if (searchType === 'InBetween') {
                            $(maskedInputsDivId).hide();
                            $(singleDateDivId).hide();
                            $(datePickersDivId).show();
                        } else {
                            $(maskedInputsDivId).hide();
                            $(datePickersDivId).hide();
                            $(singleDateDivId).show();
                        }
                        updateHiddenField();
                    });
                    updateHiddenField();
                });
            </script>");
        }
    }
}
