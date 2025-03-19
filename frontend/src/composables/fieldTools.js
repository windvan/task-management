
function getChangedFields(rawData, newData) {
  const changes = {};

  for (const key in newData) {
    // 处理嵌套对象
    // if (typeof newData[key] === "object" && newData[key] !== null) {
    //   if (JSON.stringify(newData[key]) !== JSON.stringify(rawData[key])) {
    //     changes[key] = newData[key];
    //   }
    // }
    // 处理普通字段,丢弃嵌套字段（已在editor中更新关联字段）
    if (typeof newData[key] !== "object" && newData[key] !== rawData[key]) {
      changes[key] = newData[key];
    }
  }

  return changes;
}


function getStatusSeverity(field, status) {
  // return tag severity property:
  // HintedString<"secondary" | "info" | "success" | "warn" | "danger" | "contrast">
  switch (field) {
    case "project_status":
      // "Idea_Stage" "Active" "Finished" "Terminated"
      switch (status) {
        case "Idea_Stage":
          return "secondary";
        case "Active":
          return "info";
        case "Finished":
          return "success";
        case "Terminated":
          return "warn";
        default:
          return "primary";
      }
    case "task_status":
      // "Idle""Go""Finished""Pending""Terminated"
      switch (status) {
        case "Idle":
          return "secondary";
        case "Go":
          return "info";
        case "Finished":
          return "success";
        case "Pending":
          return "contrast";
        case "Terminated":
          return "contrast";
      }
    case "payment_status":
      switch (status) {
        // Not_Start, First_Payment_Done, Full_Payment_Done
        case "Full_Payment_Done":
          return "success"
        default:
          return "warn"
      }
  }
 
}

export { getChangedFields, getStatusSeverity };
