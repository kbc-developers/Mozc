// Copyright 2010-2015, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#ifndef MOZC_COMPOSER_INTERNAL_TYPING_MODEL_H_
#define MOZC_COMPOSER_INTERNAL_TYPING_MODEL_H_

#include <memory>

#include "base/port.h"
#include "base/string_piece.h"
#include "protocol/commands.pb.h"
// for FRIEND_TEST()
#include "testing/base/public/gunit_prod.h"


namespace mozc {
namespace composer {

// TypingModel, with key-value like interface.
// The only exported interface is GetCost, which takes key
// and returns cost value.
// The key-value data source should be provided via the constructor.
// Typically the constructor taks data generated by gen_typing_model.py.
class TypingModel {
 public:
  TypingModel(const char *characters, size_t characters_size,
              const uint8 *cost_table, size_t cost_table_size,
              const int32 *mapping_table);

  virtual ~TypingModel() {}

  // Gets cost value from key.
  // virtual for mocking.
  virtual int GetCost(StringPiece key) const;

  // Gets a TypingModel based on SpecialRomanjiTable.
  // NULL if no corresponding model is available.
  static const TypingModel *GetTypingModel(
      const mozc::commands::Request::SpecialRomanjiTable
          &special_romanji_table);

  // No data means its const is infinity.
  static const int kInfinity;

  // In typing model, meaning no corresponding data.
  static const uint8 kNoData;

 private:
  FRIEND_TEST(TypingModelTest, Constructor);
  FRIEND_TEST(TypingModelTest, GetIndex);

  // Gets index from key.
  // Given cost table via the constructor is simple array
  // so when accessing to cost value, index should be
  // calculated by this method.
  // c.f. gen_typing_model.py's GetIndexFromKey.
  size_t GetIndex(StringPiece key) const;

  // Radix table, needed by GetIndex.
  std::unique_ptr<unsigned char[]> character_to_radix_table_;
  const size_t characters_size_;
  const uint8 *cost_table_;
  const size_t cost_table_size_;
  const int32 *mapping_table_;
};

}  // namespace composer
}  // namespace mozc

#endif  // MOZC_COMPOSER_INTERNAL_TYPING_MODEL_H_
