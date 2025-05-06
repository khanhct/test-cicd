const parseLastDiff = (gitDiff) => {
  gitDiff = gitDiff.replace(/\n\\ No newline at end of file/, '')
  
  const diffList = gitDiff.trimEnd().split('\n').reverse();
  const lastLineFirstChar = diffList?.[0]?.[0];
  const lastDiff =
    diffList.find((item) => {
      return /^@@ \-\d+,\d+ \+\d+,\d+ @@/g.test(item);
    }) || '';

  const [lastOldLineCount, lastNewLineCount] = lastDiff
    .replace(/@@ \-(\d+),(\d+) \+(\d+),(\d+) @@.*/g, ($0, $1, $2, $3, $4) => {
      return `${+$1 + +$2},${+$3 + +$4}`;
    })
    .split(',');
  
  if (!/^\d+$/.test(lastOldLineCount) || !/^\d+$/.test(lastNewLineCount)) {
    return {
      lastOldLine: -1,
      lastNewLine: -1,
      gitDiff,
    };
  }


  const lastOldLine = lastLineFirstChar === '+' ? null : (parseInt(lastOldLineCount) || 0) - 1;
  const lastNewLine = lastLineFirstChar === '-' ? null : (parseInt(lastNewLineCount) || 0) - 1;

  return {
    lastOldLine,
    lastNewLine,
    gitDiff,
  };
};

return parseLastDiff($input.item.json.diff)
