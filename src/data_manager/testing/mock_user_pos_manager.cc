// Copyright 2010-2016, Google Inc.
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

#include "data_manager/testing/mock_user_pos_manager.h"

#include "base/logging.h"
#include "base/singleton.h"
#include "dictionary/pos_group.h"
#include "dictionary/pos_matcher.h"
#include "dictionary/user_pos.h"

namespace mozc {
namespace testing {

MockUserPosManager *MockUserPosManager::GetUserPosManager() {
  return Singleton<MockUserPosManager>::get();
}

namespace {

// The following header file is automatically generated and contains the
// definition of variable, kPOSToken, of type UserPOSImpl::POSToken.
#include "data_manager/testing/user_pos_data.h"

}  // namespace

const dictionary::UserPOS::POSToken *
MockUserPosManager::GetUserPOSData() const {
  DCHECK(kPOSToken != NULL);
  return kPOSToken;
}

namespace {
// This header file is autogenerated by gen_pos_matcher_code.py and contains
// kRuleIdTable[] and kRangeTable[].
#include "data_manager/testing/pos_matcher_data.h"

class MockPOSMatcher : public dictionary::POSMatcher {
 public:
  MockPOSMatcher() : POSMatcher(kRuleIdTable, kRangeTables) {}
};
}  // namespace

const dictionary::POSMatcher *MockUserPosManager::GetPOSMatcher() const {
  return Singleton<MockPOSMatcher>::get();
}

}  // namespace testing
}  // namespace mozc
