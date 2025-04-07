
function toLocalStr(date) {
  // convert iso date string or Date instance to local string
  if (typeof date === 'string') {
    let _date
    if (!date.endsWith('Z')) { _date = date + 'Z' }
    return new Date(_date).toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })
  } else if (date instanceof Date) {
    return date.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })
  }
  else {
    throw new Error('Invalid date type')
  }
}
export { toLocalStr };