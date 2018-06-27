class MagicDictionary {
 public:
  /** Initialize your data structure here. */
  MagicDictionary() {
  }
  
  /** Build a dictionary through a list of words */
  void buildDict(vector<string> dict) {
    for (const string &word : dict) {
      dict_.insert(word);
    }
  }
  
  /** Returns if there is any word in the trie that equals to the given word after modifying exactly one character */
  bool search(string word) {
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      char replace_ch = word.at(i);
      for (char new_char = 'a'; new_char <= 'z'; ++new_char) {
        if (new_char == replace_ch) {
          continue;
        }
        word.at(i) = new_char;
        if (dict_.find(word) != dict_.end()) {
          return true;
        }
      }
      word.at(i) = replace_ch;
    }
    return false;
  }

 private:
  unordered_set<string> dict_;
};

/**
 * Your MagicDictionary object will be instantiated and called as such:
 * MagicDictionary obj = new MagicDictionary();
 * obj.buildDict(dict);
 * bool param_2 = obj.search(word);
 */
