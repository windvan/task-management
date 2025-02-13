<!-- 
 TODOS:
  复选框列不能冻结的问题:由首列为功能列引起，暂时无法解决
  列宽的问题
  筛选排序的问题
  在有/无筛选的条件下选择可见与选择全部 
  -->

<template>
  <div>
    <DataTable
      v-if="layout === 'list'"
      ref="outerTableRef"
      :value="tasks"
      dataKey="id"
      scrollable
      scroll-height="flex"
      resizable-columns
      column-resize-mode="expand"
      v-model:selection="selectedTasks"
      selectionMode="multiple"
      v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand"
      v-model:editingRows="editingRows"
      editMode="row"
      @rowEditSave="onRowEditSave"
      @rowEditCancel="onRowEditCancel"
      paginator
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="globalFilterFields"
      sortMode="multiple"
      removableSort
      pt:header="px-0"
    >
      <template #header>
        <Toolbar pt:start="gap-2" pt:end="gap-2">
          <template #start>
            <Button icon="pi pi-plus" label="New" @click="handleNew" severity="secondary" />
            <Button icon="pi pi-trash" label="Delete" @click="handleDelete" severity="secondary" />
          </template>

          <template #center>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <InputText placeholder="Search" v-model="filters['global'].value" />
            </IconField>
          </template>

          <template #end>
            <Button
              icon="pi pi-cog"
              rounded
              severity="secondary"
              v-tooltip.top="'Select columns'"
              @click="toggleColsPopover"
            ></Button>

            <Popover ref="colsPopoverRef" @show="onPopoverShow" pt:content="flex flex-col gap-4">
              <div class="flex gap-8 justify-center">
                <Button
                  label="Apply"
                  icon="pi pi-check"
                  variant="outlined"
                  size="small"
                  @click="onApply"
                ></Button>
                <Button
                  label="Cancel"
                  icon="pi pi-times"
                  severity="secondary"
                  size="small"
                  @click="onCancel"
                ></Button>
                <Button
                  label="Default"
                  icon="pi pi-undo"
                  severity="secondary"
                  size="small"
                  @click="onDefault"
                ></Button>
              </div>
              <PickList
                v-model="columnPicker"
                dataKey="idx"
                breakpoint="800px"
                scroll-height="20rem"
              >
                <template #option="{ option }">
                  {{ option.col }}
                </template>
                <template #sourceheader>
                  <span class="font-bold">All Columns</span>
                  <hr />
                </template>
                <template #targetheader>
                  <span class="font-bold">Selected Columns</span>
                  <hr />
                </template>
              </PickList>
              <div class="flex items-center gap-2">
                <Checkbox v-model="rememberSelection" binary inputId="remember" size="small" />
                <label for="remember"> Remember my selection</label>
              </div>
            </Popover>

            <SelectButton
              v-model="layout"
              :options="['list', 'grid']"
              :allowEmpty="false"
              v-tooltip.top="'Toggle display list/grid'"
            >
              <template #option="{ option }">
                <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
              </template>
            </SelectButton>
            <SplitButton
              severity="secondary"
              label="Export"
              icon="pi pi-download"
              @click="handleExport"
              :model="splitBtnItems"
            >
            </SplitButton>
          </template>
        </Toolbar>
      </template>

      <!-- <Column v-if="field in visibleColumns" expander class="w-12" frozen /> -->
      <Column expander frozen />
      <!-- <Column frozen selectionMode="multiple"></Column> -->

      <Column
        v-if="visibleColumns.has('project_id')"
        field="project_id"
        header="Project Name"
        header-class="min-w-48"
        frozen
        sortable
      >
        <template #body="{ data, field }">
          {{ selectOptions?.projectOptions?.find((proj) => proj.id === data[field])?.project_name }}
        </template>
        <template #filter="{ filterModel }">
          <InputText v-model="filterModel.value" type="text" placeholder="Search by country" />
        </template>
      </Column>

      <Column
        v-if="visibleColumns.has('task_name')"
        field="task_name"
        header="Task Name"
        header-class="min-w-48"
        class="border-r border-r-gray-300"
        frozen
        sortable
      >
        <template #body="{ data, field }">
          <Button
            :label="data[field]"
            variant="link"
            @click="handleEdit(data)"
            class="px-0 text-left"
          ></Button>
        </template>
        <!-- <template #editor="{data,field}">
          <InputText v-model="data[field]"></InputText>
        </template> -->
      </Column>
      <Column
        filter-field=""
        v-if="visibleColumns.has('task_category')"
        field="task_category"
        header="Task Category"
        sortable
        header-class="min-w-40"
      ></Column>
      <Column v-if="visibleColumns.has('tags')" field="tags" header="Tags">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputText>
        </template>
      </Column>

      <Column v-if="visibleColumns.has('task_status')" field="task_status" header="Task Status">
        <template #body="{ data, field }">
          <Tag :severity="getTaskStatusSeverity(data[field])" :value="data[field]"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Select
            :options="enums.TaskStatusEnum"
            class="w-full"
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </Select>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('start_year')"
        field="start_year"
        header="Start Year"
        :pt="{ headerCell: ({ parent }) => ({ class: { 'min-w-48': parent.state['d_editing'] } }) }"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            view="year"
            date-format="yy"
            :min-date="new Date()"
            :model-value="new Date(data[field], 0)"
            @update:model-value="(value) => onCellChange(data.id, field, value?.getFullYear())"
          />
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('expected_delivery_date')"
        field="expected_delivery_date"
        header="Expected Delivery Date"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="new Date(data[field])"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column v-if="visibleColumns.has('task_owner_id')" field="task_owner_id" header="Task Owner">
        <template #body="{ data, field }">
          {{ selectOptions?.userOptions?.find((user) => user.id === data[field])?.name }}
        </template>
        <template #editor="{ data, field }">
          <Select
            :options="selectOptions?.userOptions"
            option-label="name"
            :model-value="selectOptions?.userOptions?.find((user) => user.id === data[field])"
            @update:model-value="(value) => onCellChange(data.id, field, value.id)"
          ></Select>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('crop')" field="crop" header="Crop">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputText>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('target')" field="target" header="Target">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputText>
        </template>
      </Column>

      <Column
        v-if="visibleColumns.has('task_confirmed')"
        field="task_confirmed"
        header="Task Confirmed"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>

        ></Column
      >
      <Column
        v-if="visibleColumns.has('budget_confirmed')"
        field="budget_confirmed"
        header="Budget Confirmed"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('cost_center')" field="cost_center" header="Cost Center">
        <template #editor="{ data, field }">
          <Select
            :options="enums.CostCenterEnum"
            class="w-full"
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </Select>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('tox_gov_approved')"
        field="tox_gov_approved"
        header="Tox_Gov Approved"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('ecotox_gov_approved')"
        field="ecotox_gov_approved"
        header="EcoTox_Gov Approved"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('pi_number')" field="pi_number" header="PI NO.">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputText> </template
      ></Column>
      <Column v-if="visibleColumns.has('tk_number')" field="tk_number" header="TK NO.">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText> </template
      ></Column>
      <!-- gap is not necessary and mainly for scoping tasks -->
      <Column v-if="visibleColumns.has('gap_snapshot')" field="gap_snapshot" header="GAP Sanpshot">
        <template #body="{ data, field, index }">
          <a
            @click.prevent="onGapViewShow(data.id, data[field], index)"
            class="text-primary hover:underline"
            >{{ data[field] ? 'Show' : 'Add' }}</a
          >
        </template>
      </Column>
      <Column v-if="visibleColumns.has('doc_link')" field="doc_link" header="Doc Link">
        <template #body="{ data, field }">
          <a
            v-if="data[field]"
            class="text-primary hover:underline"
            :href="data[field]"
            target="_blank"
            >Follow</a
          >
        </template>
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputText>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('estimated_cost')"
        field="estimated_cost"
        header="Estimated Cost"
      >
        <template #body="{ data, field }">
          {{ data[field] ? `&yen; ${data[field]}` : null }}
        </template>
        <template #editor="{ data, field }">
          <InputNumber
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputNumber>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('actual_cost')" field="actual_cost" header="Actual Cost">
        <template #body="{ data, field }">
          {{ data[field] ? `￥${data[field]}` : null }}
        </template>
        <template #editor="{ data, field }">
          <InputNumber
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputNumber>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('po_placed')" field="po_placed" header="PO Placed">
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('contract_signed')"
        field="contract_signed"
        header="Contract Signed"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('payment_method')"
        field="payment_method"
        header="Payment Method"
      >
        <template #editor="{ data, field }">
          <Select
            :options="enums.PaymentMethodEnum"
            class="w-full"
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </Select>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('payment_status')"
        field="payment_status"
        header="Payment Status"
      >
        <template #editor="{ data, field }">
          <Select
            :options="enums.PaymentStatusEnum"
            class="w-full"
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </Select>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('vv_doc_uploaded')"
        field="vv_doc_uploaded"
        header="Veeva Uploaded"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('vv_doc_number')"
        field="vv_doc_number"
        header="Veeva Doc Number"
      >
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText>
        </template>
      </Column>

      <Column
        v-if="visibleColumns.has('task_progress')"
        field="task_progress"
        header="Task Progress"
      >
        <template #editor="{ data, field }">
          <Select
            :options="enums.TaskProgressEnum"
            class="w-full"
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </Select> </template
      ></Column>
      <Column
        v-if="visibleColumns.has('planned_start')"
        field="planned_start"
        header="Planned Start"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('expected_finish')"
        field="expected_finish"
        header="Expected Finish"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column v-if="visibleColumns.has('actual_start')" field="actual_start" header="Actual Start">
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('actual_finish')"
        field="actual_finish"
        header="Actual Finish"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('delivery_date')"
        field="delivery_date"
        header="Delivery Date"
      >
        <template #editor="{ data, field }">
          <DatePicker
            showIcon
            iconDisplay="input"
            showButtonBar
            date-format="yy-mm-dd"
            :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null"
            @update:model-value="(value) => onCellChange(data.id, field, dateToStr(value))"
          />
        </template>
      </Column>
      <Column v-if="visibleColumns.has('stuff_days')" field="stuff_days" header="Stuff Days">
        <template #editor="{ data, field }">
          <InputNumber
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></InputNumber>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('cro_id')" field="cro_id" header="CRO Name">
        <template #body="{ data, field }">
          {{ selectOptions?.croOptions?.find((cro) => cro.id === data[field])?.cro_name }}
        </template>
        <template #editor="{ data, field }">
          <Select
            :options="selectOptions?.croOptions"
            option-label="cro_name"
            :model-value="selectOptions?.croOptions?.find((cro) => cro.id === data[field])"
            @update:model-value="(value) => onCellChange(data.id, field, value.id)"
          ></Select>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('samples')" field="samples" header="Sample Status">
        <template #body="{ data, field }">
          <a @click.prevent="onSamplesViewShow(data.id)">
            <template v-if="data[field].length > 0"
              ><Tag
                v-for="(sample, index) in data[field]"
                :value="sample.sample_status"
                :Key="index"
                class="hover:underline"
              />
            </template>
            <span v-else class="text-primary hover:underline">Add</span>
          </a>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('study_notified')"
        field="study_notified"
        header="Study Notified"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>

      <Column v-if="visibleColumns.has('analytes')" field="analytes" header="Analytes">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText>
        </template>
      </Column>

      <Column v-if="visibleColumns.has('key_results')" field="key_results" header="Key Results">
        <template #body="{ data, field, index }">
          <a
            @click.prevent="onKeyResultsViewShow(data.id, data[field], index)"
            class="text-primary hover:underline"
            >Show</a
          >
        </template>
      </Column>
      <Column v-if="visibleColumns.has('guidelines')" field="guidelines" header="Guidelines">
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('test_item_info_sent')"
        field="test_item_info_sent"
        header="Test Item Info Sent"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('ssd_finished')" field="ssd_finished" header="SSD Finished">
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleColumns.has('sed_uploaded')" field="sed_uploaded" header="SED Uploaded">
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox
            binary
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          ></Checkbox>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('global_study_manager')"
        field="global_study_manager"
        header="Global Study Manager"
      >
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText>
        </template>
      </Column>
      <Column
        v-if="visibleColumns.has('cro_study_director')"
        field="cro_study_director"
        header="CRO Study Director"
      >
        <template #editor="{ data, field }">
          <InputText
            :model-value="data[field]"
            @update:model-value="(value) => onCellChange(data.id, field, value)"
          >
          </InputText> </template
      ></Column>

      <Column
        rowEditor
        class="border-l border-l-gray-300 text-center p-2"
        frozen
        align-frozen="right"
        :pt="{
          columnHeaderContent: 'justify-center',
          pcRowEditorInit: { root: 'size-7' },
          pcRowEditorSave: { root: 'size-7' },
          pcRowEditorCancel: { root: 'size-7' },
          headerCell: ({ parent }) => ({
            class: parent.state['d_editing'] ? 'min-w-16' : 'min-w-8'
          })
        }"
      >
        <template #header>
          <Button
            icon="pi pi-pencil"
            v-show="!editingRows.length"
            rounded
            class="size-7"
            size="small"
            severity="secondary"
            @click="onToggleRowEditAll"
          />
          <Button
            icon="pi pi-times"
            v-show="editingRows.length"
            rounded
            class="size-7"
            size="small"
            severity="secondary"
            @click="onRowEditCancelAll"
          />
          <Button
            icon="pi pi-check"
            v-show="editingRows.length"
            rounded
            class="size-7"
            size="small"
            severity="secondary"
            @click="onRowEditSaveAll"
          />
        </template>
      </Column>
      <Column frozen align-frozen="right" header=" " class="text-center p-2" header-class="w-8">
        <template #body="{ data }">
          <Button
            severity="secondary"
            rounded
            class="size-7"
            size="small"
            icon="pi pi-comments"
            @click="showComments(data)"
          ></Button>
        </template>
      </Column>
      <template #empty>
        <p class="text-center text-primary">No tasks Found!</p>
      </template>
    </DataTable>

    <Dialog
      v-model:visible="gapViewvisible"
      modal
      maximizable
      header="Gap Snapshots"
      :style="{ width: '80rem' }"
    >
      <div class="flex flex-col gap-4">
        <div
          v-for="(gap, index) in currentTaskGaps.gapURLs"
          :key="index"
          class="border rounded-md p-2"
        >
          <div class="flex items-center gap-4 mb-2">
            <span>{{ index + 1 }} </span>
            <span>{{ gap.split('/').pop() }}</span>
            <Button
              icon="pi pi-times"
              rounded
              severity="warn"
              variant="outlined"
              class="size-8"
              @click="onGapDelete(currentTaskGaps.task_id, gap)"
            ></Button>
          </div>
          <!-- <img :src="apiBaseStaticUrl + gap" class=" max-w-full max-h-96 object-contain rounded" /> -->
          <Image
            :src="apiBaseStaticUrl + gap"
            class="h-64"
            preview
            pt:originalContainer="max-w-full overflow-auto"
          />
        </div>
        <FileUpload
          name="gap_snapshot"
          customUpload
          @uploader="onGapUpload"
          accept="image/*"
          :maxFileSize="1048576"
        >
          <template #empty>
            <span>Drag and drop image to here to upload.</span>
          </template>
        </FileUpload>
        <pre>{{ currentTaskGaps }}</pre>
      </div>
    </Dialog>
    <Dialog
      v-model:visible="keyResultsvisible"
      modal
      maximizable
      header="Key Results"
      :style="{ width: '80rem' }"
    >
      <div class="flex flex-col gap-4">
        <pre>{{ currentTaskKeyResults }}</pre>
      </div>
    </Dialog>
    <Dialog
      v-model:visible="samplesViewVisible"
      modal
      maximizable
      header="Task Samples"
      :style="{ width: '80rem' }"
    >
      <pre>{{ currentTaskSamples }}</pre>
    </Dialog>

    <Drawer v-model:visible="commentsViewVisible" position="right" class="w-[40rem]">
      <template #header>
        <div class="flex items-center gap-2">
          <span class="font-bold">header="Task Comments"</span>
        </div>
      </template>

      <template #footer>
        <div class="flex items-center gap-2">
          <Button label="Account" icon="pi pi-user" class="flex-auto" outlined></Button>
          <Button
            label="Logout"
            icon="pi pi-sign-out"
            class="flex-auto"
            severity="danger"
            text
          ></Button>
        </div>
      </template>
      <pre
        >{{ currentTask }}
      </pre>
    </Drawer>

    <ConfirmDialog></ConfirmDialog>

    <CreatTasks
      v-if="showCreateForm"
      v-model:visible="showCreateForm"
      @refresh="refreshTasks"
    ></CreatTasks>

    <EditTask
      v-if="showEditForm"
      v-model:visible="showEditForm"
      :initialFormData="initialFormData"
      @refresh="refreshTasks"
    ></EditTask>
    <template v-if="layout === 'grid'">
      <SelectButton v-model="layout" :options="['list', 'grid']" :allowEmpty="false">
        <template #option="{ option }">
          <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
        </template>
      </SelectButton>
      <TaskCard v-for="task of tasks" :key="task.id" :task-data="task"></TaskCard>
    </template>
  </div>
</template>

<script setup>
  import { onMounted, inject, ref, useTemplateRef, toRaw } from 'vue'

  import { useToast } from 'primevue/usetoast'
  import { useConfirm } from 'primevue/useconfirm'
  import { FilterMatchMode } from '@primevue/core'


  import { dateToStr } from '@/composables/dateTools'
  import EditTask from './EditTask.vue'
  import CreatTasks from './CreatTasks.vue'
  import TaskCard from './TaskCard.vue'

  const apiBaseStaticUrl = import.meta.env.VITE_API_BASE_STATIC_URL

  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
  const layout = ref('list')
  const toast = useToast()
  const confirm = useConfirm()
  const $axios = inject('$axios')
  const outerTableRef = useTemplateRef('outerTableRef')
  const colsPopoverRef = useTemplateRef('colsPopoverRef')
  const gapViewvisible = ref(false)
  const keyResultsvisible = ref(false)
  const samplesViewVisible = ref(false)
  const currentTaskSamples = ref()
  const currentTaskGaps = ref()
  const currentTaskKeyResults = ref()
  let currentTask //for showing comments, id needed

  const tasks = ref([])
  const expandedRows = ref([])
  const selectedTasks = ref([])
  const showCreateForm = ref(false)
  const showEditForm = ref(false)
  const splitBtnItems = [{ label: 'Import', icon: 'pi pi-upload', command: handleImport }]
  let initialFormData
  const selectOptions = ref()
  const globalFilterFields = ['porject_id', 'task_name', 'tags']

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    task_category: { value: null, matchMode: FilterMatchMode.EQUALS },
    project_id: { value: null, matchMode: FilterMatchMode.EQUALS }
    // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
  })

  const columnPicker = ref(null)
  const visibleColumns = ref(new Set())

  const rememberSelection = ref(true)
  let updatedTasks = {}

  let defaultCol = [
    'project_id',
    'task_name',
    'tags',
    'task_owner_id',
    'task_confirmed',
    'task_status',
    'start_year',
    'expected_delivery_date',
    'pi_number',
    'tk_number',
    'tox_gov_approved',
    'ecotox_gov_approved'
  ]
  // requiredCol must be a subset of defaultCol
  let requiredCol = [
    'project_id',
    'task_name',
    'tags',
    'task_owner_id',
    'task_confirmed',
    'task_status',
    'start_year',
    'expected_delivery_date'
  ]

  const editingRows = ref([])
  const commentsViewVisible = ref(false)

  async function showComments(data) {
    commentsViewVisible.value = true
    try {
      // let response = await $axios.get(`/comments/${data.id}`)
      // currentTask = response.data
      currentTask = data
    } catch (err) {
      console.log('Get Task Comments Error!', err)
    }
  }

  onMounted(async () => {

      tasks.value = await $axios.get('/tasks/') // errors will be handled globally
       


    // load visibleColumns from localstorage: [col1,col2,col3...]

    let cachedCol = localStorage.getItem('taskVisibleColumns')

    if (cachedCol) {
      visibleColumns.value = new Set([...JSON.parse(cachedCol), ...requiredCol])
    } else {
      visibleColumns.value = new Set(defaultCol)
    }
  })

  //get select options if enter edit mode
  onMounted(async () => {
    try {
      let response = await $axios.get('/tasks/select-options')
      selectOptions.value = response.data
    } catch (err) {
      console.log('get select options failed on tasks edit view', err)
    }
  })

  function onGapViewShow(task_id, gap_snapshot, index) {
    currentTaskGaps.value = { task_id, index, gapURLs: gap_snapshot?.split(',') ?? [] }
    gapViewvisible.value = true
  }
  function onKeyResultsViewShow(task_id, results, index) {
    currentTaskKeyResults.value = { task_id, results, index }
    keyResultsvisible.value = true
  }

  async function onSamplesViewShow(task_id) {
    samplesViewVisible.value = true
    try {
      let response = await $axios.get(`/tasks/${task_id}/samples`)
      currentTaskSamples.value = response.data
    } catch (error) {
      console.log('get task samples error', error)
    }

    // currentTaskSamples.value = { task_id, samples }
  }
  async function onGapUpload(event) {
    const formData = new FormData()

    event.files.forEach((file) => {
      formData.append('files', file)
    })

    try {
      let response = await $axios.post(`/tasks/gaps/${currentTaskGaps.value.task_id}`, formData)
      currentTaskGaps.value.gapURLs = response.data.gap_snapshot.split(',')
      tasks.value[currentTaskGaps.value.index].gap_snapshot = response.data.gap_snapshot
    } catch (error) {
      console.log(error)
    }
  }

  async function onGapDelete(task_id, gap) {
    try {
      let response = await $axios.delete(`/tasks/gaps/${task_id}`, { params: { gap_path: gap } })
      console.log(response.data)
      currentTaskGaps.value.gapURLs = response.data.gap_snapshot?.split(',')
      tasks.value[currentTaskGaps.value.index].gap_snapshot = response.data.gap_snapshot
    } catch (error) {
      console.log(error)
    }
  }

  function toggleColsPopover(event) {
    colsPopoverRef.value?.toggle(event)
  }

  function getTaskStatusSeverity(status) {
    switch (status) {
      case 'Idle':
        return 'secondary'
      case 'Go':
        return 'info'
      case 'Finished':
        return 'success'
      case 'Pending':
        return 'danger'
      case 'Terminated':
        return 'danger'
      default:
        return 'primary' // 或者其他默认值
    }
  }

  function setColumnPicker(visibleColumns) {
    // this fucntion accepts a Set type argument

    // get all columns list:[{idx:number,col:string}]
    let allCols = Object.keys(tasks.value[0] ?? {}).map((col, idx) => {
      return { idx, col }
    })

    // set columnpicker based on current visiblecolumns
    let targetCols = []
    let sourceCols = []

    allCols.forEach((item) => {
      if (visibleColumns.has(item.col)) {
        targetCols.push(item)
      } else {
        sourceCols.push(item)
      }
    })
    columnPicker.value = [sourceCols, targetCols]
  }
  function onPopoverShow() {
    setColumnPicker(visibleColumns.value)
  }

  function onApply() {
    visibleColumns.value = new Set(columnPicker.value[1].map((item) => item.col))
    colsPopoverRef.value.hide()

    if (rememberSelection.value) {
      localStorage.setItem('taskVisibleColumns', JSON.stringify(Array.from(visibleColumns.value)))
    } else {
      localStorage.removeItem('taskVisibleColumns')
    }
  }

  function onCancel() {
    //reset columnpicker based on current visiblecolumns
    // columnPicker.value[1] = visibleColumns.value.map((col) => {
    //   return { idx: columnPicker.value[0].find((item) => item.col === col).idx, col: col }
    // })
    colsPopoverRef.value.hide()
  }

  function onDefault() {
    setColumnPicker(new Set(defaultCol))
  }
  async function onRowExpand(event) {
    console.log('onRowExpand', event)
  }

  function handleImport() {
    toast.add({
      severity: 'warn',
      summary: 'Warn Message',
      detail: 'To be implemented',
      life: 3000
    })
  }

  function handleExport() {
    outerTableRef.value.exportCSV()
  }

  function handleEdit(row) {
    initialFormData = toRaw(row)
    showEditForm.value = true
  }

  function handleNew() {
    showCreateForm.value = true
  }

  function onCellChange(task_id, field, value) {
    if (task_id in updatedTasks) {
      updatedTasks[task_id][field] = value
    } else {
      updatedTasks[task_id] = { [field]: value }
    }
  }

  async function onRowEditSave(event) {
    try {
      await $axios.patch('/tasks/', { [event.data.id]: updatedTasks[event.data.id] })
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Update task successfully',
        life: 3000
      })
      delete updatedTasks[event.data.id]
      await refreshTasks()
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: `Update task failed: ${event.data.id}`,
        life: 3000
      })
      console.log(error)
    }
  }
  async function onRowEditSaveAll() {
    try {
      await $axios.patch('/tasks/', updatedTasks)
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Update task successfully',
        life: 3000
      })
      updatedTasks = {}
      editingRows.value = []

      await refreshTasks()
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Update tasks failed',
        life: 3000
      })
      console.log(error)
    }
  }

  function onRowEditCancel(event) {
    delete updatedTasks[event.data.id]
  }
  function onToggleRowEditAll() {
    // edit selected rows
    if (selectedTasks.value.length) {
      editingRows.value = selectedTasks.value
    } else {
      toast.add({
        severity: 'warn',
        summary: 'Warning!',
        detail: 'Please select rows first!',
        life: 3000
      })
    }
  }

  function onRowEditCancelAll() {
    updatedTasks = {}
    editingRows.value = []
  }

  async function handleDelete() {
    if (!selectedTasks.value.length) {
      toast.add({
        severity: 'warn',
        summary: 'Warning!',
        detail: 'Please select rows first!',
        life: 2000
      })
      return
    }
    confirm.require({
      position: 'top',
      message: 'Sure to delete selected tasks?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      rejectProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true
      },
      acceptProps: {
        label: 'Confirm'
      },
      accept: async () => {
        let response
        let task_ids
        if (selectedTasks.value.length === 1) {
          task_ids = selectedTasks.value[0].id
        } else {
          task_ids = selectedTasks.value.map((task) => task.id)
        }
        try {
          response = await $axios.delete(`/tasks/`, { data: task_ids })
          console.log(response.data)
        } catch (error) {
          console.error('Error deleting tasks:', error)
        }

        //refresh products
        try {
          response = await $axios.get('/tasks/')
          tasks.value = response.data
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: response.data.message,
            life: 3000
          })
        } catch (err) {
          toast.add({ severity: 'error', summary: 'Error', detail: err.message })
        }
        selectedTasks.value = null
      },
      reject: () => {}
    })
  }

  async function refreshTasks() {
    try {
      const response = await $axios.get('/tasks/')
      tasks.value = response.data
    } catch (err) {
      console.error(err)
    }
  }
</script>

<style module></style>

<style>
  /* resolve inline edit control display over frozen column when scroll */
  .p-datatable-thead {
    z-index: 2;
  }
  .p-datatable-frozen-column {
    z-index: 1;
  }
</style>
