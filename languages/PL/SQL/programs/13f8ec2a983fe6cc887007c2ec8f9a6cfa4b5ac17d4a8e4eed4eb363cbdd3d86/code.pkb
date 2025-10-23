create or replace package body ut_be_true_matcher is

  /*
  utPLSQL - Version 3
  Copyright 2016 - 2021 utPLSQL Project

  Licensed under the Apache License, Version 2.0 (the "License"):
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  */

  function process_expectation(a_expectation in out nocopy ut_expectation) return ut_expectation_result is
    l_result ut_expectation_result;
    l_passed boolean;
  begin
    l_passed := (a_expectation.actual.data_value is not null and a_expectation.actual.data_value.is_boolean() and a_expectation.actual.to_boolean());
    if l_passed = a_expectation.to_be_not then
      a_expectation.message := ut_utils.tr(
        'ut_be_true_failure'
        ,coalesce(ut_utils.to_string(a_expectation.actual), 'NULL')
        ,case when a_expectation.to_be_not then '' else ut_utils.tr('ut_not') end
      );
    end if;
    l_result := ut_expectation_result(a_passed => (l_passed != a_expectation.to_be_not));
    return l_result;
  end;

end ut_be_true_matcher;
/
