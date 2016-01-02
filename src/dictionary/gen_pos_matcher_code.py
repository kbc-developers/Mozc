# -*- coding: utf-8 -*-
# Copyright 2010-2016, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""A tool to generate POS matcher."""

__author__ = "taku"

import optparse
import re
import sys

from dictionary import pos_util


def OutputPosMatcherData(pos_matcher, output):
  """Generates the data used by POSMatcher.

  Two data arrays are generated:
    1) const uint16 kRuleIdTable[]
       This contains POS ID for each rule in pos_matcher_rule.def. The data is
       used by the method Get<RuleName>() generated by this script. Each array
       index corresponds to one rule name in its declared order. Namely, if
       pos_matcher_rule.def contain three rules, say
         Rule0  Regexp0
         Rule1  Regexp1
         Rule2  Regexp2
       Then kRuleIdTable[0] contains the result of GetRule0(), etc.

    2) const POSMatcher::Range kRangeTable[]
       Each element is a pointer to another array containing ranges of POS IDs
       whose union is the set of all POS IDs that match the regexp. Each array
       of ranges ends with the endmark { 0xFFFF, 0xFFFF }.

  Generated data can be passed to POSMatcher, which is also generated by
  this script, to get a POSMatcher corresponding to given data set.
  """

  # Generate kRuleIdTable[].
  output.write('const uint16 kRuleIdTable[] = {\n')
  for rule_name in pos_matcher.GetRuleNameList():
    output.write(
        '  %(id)4d,  // %(rule_name)s "%(original_pattern)s"\n'
        % { 'id': pos_matcher.GetId(rule_name),
            'rule_name': rule_name,
            'original_pattern': pos_matcher.GetOriginalPattern(rule_name) })
  output.write('  static_cast<uint16>(0xFFFF),\n')
  output.write('};\n')

  # Generate arrays of ranges each of which will be an element of kRangeTable[].
  output.write('namespace {\n')
  for rule_name in pos_matcher.GetRuleNameList():
    output.write(
        '// %(rule_name)s "%(original_pattern)s"\n'
        'const ::mozc::dictionary::POSMatcher::Range '
        'kRangeTable_%(rule_name)s[] = {\n'
        % { 'rule_name': rule_name,
            'original_pattern': pos_matcher.GetOriginalPattern(rule_name) })
    for id_range in pos_matcher.GetRange(rule_name):
      output.write('  { %4d, %4d },\n' % id_range)
    # End mark for this array of ranges.
    output.write(
        '  { static_cast<uint16>(0xFFFF), static_cast<uint16>(0xFFFF) },\n'
        '};\n')
  output.write('}  // namespace\n')

  # Generate kRangeTable[].
  output.write(
      'const ::mozc::dictionary::POSMatcher::Range *const '
      'kRangeTables[%d] = {\n'
      % (len(pos_matcher.GetRuleNameList()) + 1))
  for rule_name in pos_matcher.GetRuleNameList():
    output.write('  kRangeTable_%s,\n' % rule_name)
  output.write('  NULL,\n')
  output.write('};\n')


def OutputPosMatcherHeader(pos_matcher, output):
  """Generates the definition of POSMatcher class.

  POSMatcher is independent of the actual input data but just provides logic
  for POS matching. To use a generated class, it's required to pass two arrays,
  kRuleIdTable[] and kRangeTables[], to the constructor of POSMatcher.
  """

  output.write(
      '#ifndef MOZC_DICTIONARY_POS_MATCHER_H_\n'
      '#define MOZC_DICTIONARY_POS_MATCHER_H_\n'
      '#include "./base/port.h"\n'
      'namespace mozc {\n'
      'namespace dictionary {\n'
      'class POSMatcher {\n'
      ' public:\n'
      '  struct Range {\n'
      '    uint16 lower;\n'
      '    uint16 upper;\n'
      '  };\n')

  # Helper function to generate Get<RuleName>Id() method from rule name and its
  # corresponding index.
  def _GenerateGetMethod(rule_name, index):
    return ('  inline uint16 Get%(rule_name)sId() const {\n'
            '    return rule_id_table_[%(index)d];\n'
            '  }' % { 'rule_name': rule_name, 'index': index })

  # Helper function to generate Is<RuleName>(uint16 id) method from rule name
  # and its corresponding index. The generated function checks if the given id
  # belongs to some range in kRangeTable[index] = kRangeTable_RuleName[].
  def _GenerateIsMethod(rule_name, index):
    return ('  inline bool Is%(rule_name)s(uint16 id) const {\n'
            '    for (const Range *range = range_table_[%(index)d];\n'
            '         range->lower != static_cast<uint16>(0xFFFF); ++range) {\n'
            '      if (id >= range->lower && id <= range->upper) {\n'
            '        return true;\n'
            '      }\n'
            '    }\n'
            '    return false;\n'
            '  }' % { 'rule_name': rule_name, 'index': index })

  # Generate Get<RuleName>Id() and Is<RuleName>(uint16 id) for each rule.
  for i, rule_name in enumerate(pos_matcher.GetRuleNameList()):
    output.write(
        '  // %(rule_name)s "%(original_pattern)s"\n'
        '%(get_method)s\n'
        '%(is_method)s\n' % {
            'rule_name': rule_name,
            'original_pattern': pos_matcher.GetOriginalPattern(rule_name),
            'get_method': _GenerateGetMethod(rule_name, i),
            'is_method': _GenerateIsMethod(rule_name, i) })

  # Constructor takes two pointers to arrays generated by OutputPosMatcherData()
  # function.
  output.write(
      ' public:\n'
      '  POSMatcher(const uint16 *const rule_id_table,\n'
      '             const Range *const *const range_table)\n'
      '      : rule_id_table_(rule_id_table),\n'
      '        range_table_(range_table) {}\n'
      ' private:\n'
      '  const uint16 *const rule_id_table_;\n'
      '  const Range *const *const range_table_;\n'
      '};\n'
      '}  // namespace dictionary\n'
      '}  // namespace mozc\n'
      '#endif  // MOZC_DICTIONARY_POS_MATCHER_H_\n')


def ParseOptions():
  parser = optparse.OptionParser()
  parser.add_option('--id_file', dest='id_file', help='Path to id.def')
  parser.add_option('--special_pos_file', dest='special_pos_file',
                    help='Path to special_pos.def')
  parser.add_option('--pos_matcher_rule_file', dest='pos_matcher_rule_file',
                    help='Path to pos_matcher_rule.def')
  parser.add_option('--output_pos_matcher_data',
                    dest='output_pos_matcher_data',
                    default='',
                    help='Path to the output header file of pos matcher data.')
  parser.add_option('--output_pos_matcher_h',
                    dest='output_pos_matcher_h',
                    default='',
                    help='Path to the output header file of POSMatcher.')
  return parser.parse_args()[0]


def main():
  options = ParseOptions()

  if options.output_pos_matcher_h:
    # To generate a header file of POSMatcher, you don't need to specify
    # --id_file and --special_pos_file because empty POS database sufficies.
    pos_database = pos_util.PosDataBase()
    pos_matcher = pos_util.PosMatcher(pos_database)
    pos_matcher.Parse(options.pos_matcher_rule_file)
    with open(options.output_pos_matcher_h, 'w') as stream:
      OutputPosMatcherHeader(pos_matcher, stream)

  if options.output_pos_matcher_data:
    pos_database = pos_util.PosDataBase()
    pos_database.Parse(options.id_file, options.special_pos_file)
    pos_matcher = pos_util.PosMatcher(pos_database)
    pos_matcher.Parse(options.pos_matcher_rule_file)
    with open(options.output_pos_matcher_data, 'w') as stream:
      OutputPosMatcherData(pos_matcher, stream)


if __name__ == "__main__":
  main()
