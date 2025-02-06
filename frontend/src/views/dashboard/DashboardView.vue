<template>
  <div class="dashboard-container">
    <div class="statistics">
      <div class="card">
        <Chart type="bar" :data="barChartData" :options="barChartOptions"></Chart>
      </div>
      <div class="card">
        <Chart type="pie" :data="pieChartData" :options="pieChartOptions"></Chart>
      </div>
      <div class="card">
        <Chart type="bar" :data="stackChartData" :options="stackChartOptions"></Chart>
      </div>
      <div class="card">
        <Chart type="polarArea" :data="polarChartData" :options="polarChartOptions"></Chart>
      </div>
    </div>
    <Divider></Divider>
    <!-- <div class="tasks"> -->
    <Accordion :multiple="true" :value="expanded_item">
      <AccordionPanel value="0" class="custom-panel">
        <AccordionHeader class="custom-header">Studies</AccordionHeader>
        <AccordionContent>
          <DataTable :value="studies" stripedRows paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
            tableStyle="min-width: 50rem">
            <Column field="category" header="category" style="width: 25%"></Column>
            <Column field="start_year" header="start_year" style="width: 25%"></Column>
            <Column field="task_owner" header="task_owner" style="width: 25%"></Column>
            <Column field="expected_delivery" header="expected_delivery" style="width: 25%"></Column>
            <Column field="registration_type" header="registration_type" style="width: 25%"></Column>
            <Column field="contract_signed" header="contract_signed" style="width: 25%"></Column>
            <Column field="task_progress" header="task_progress" style="width: 25%"></Column>
          </DataTable>

        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="1" class="custom-panel">
        <AccordionHeader class="custom-header">Risk Assessments</AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam
            rem
            aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
            explicabo.
            Nemo enim
            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos
            qui ratione voluptatem sequi nesciunt. Consectetur, adipisci velit, sed quia non numquam eius modi.
          </p>
        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="2" class="custom-panel">
        <AccordionHeader class="custom-header">Unplanned Requests</AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti
            atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique
            sunt in culpa
            qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et
            expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo
            minus.
          </p>
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
    <!-- </div> -->
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue";
  const expanded_item = ref(["0", "1"])

  onMounted(() => {
    barChartData.value = setBarChartData();
    barChartOptions.value = setBarChartOptions();
    pieChartData.value = setPieChartData();
    pieChartOptions.value = setPieChartOptions();
    stackChartData.value = setStackChartData();
    stackChartOptions.value = setStackChartOptions();
    polarChartData.value = setPolarChartData();
    polarChartOptions.value = setPolarChartOptions();

  });

  const barChartData = ref();
  const barChartOptions = ref();
  const pieChartData = ref();
  const pieChartOptions = ref();
  const stackChartData = ref();
  const stackChartOptions = ref();
  const polarChartData = ref();
  const polarChartOptions = ref();

  const setBarChartData = () => {
    return {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [
        {
          label: 'Sales',
          data: [540, 325, 702, 620],
          backgroundColor: ['rgba(249, 115, 22, 0.2)', 'rgba(6, 182, 212, 0.2)', 'rgb(107, 114, 128, 0.2)', 'rgba(139, 92, 246 0.2)'],
          borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
          borderWidth: 1
        }
      ]
    };
  };
  const setBarChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        }
      }
    };
  }
  const setPieChartData = () => {
    const documentStyle = getComputedStyle(document.body);

    return {
      labels: ['A', 'B', 'C'],
      datasets: [
        {
          data: [540, 325, 702],
          backgroundColor: [documentStyle.getPropertyValue('--p-cyan-500'), documentStyle.getPropertyValue('--p-orange-500'), documentStyle.getPropertyValue('--p-gray-500')],
          hoverBackgroundColor: [documentStyle.getPropertyValue('--p-cyan-400'), documentStyle.getPropertyValue('--p-orange-400'), documentStyle.getPropertyValue('--p-gray-400')]
        }
      ]
    };
  };
  const setPieChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');

    return {
      plugins: {
        legend: {
          labels: {
            usePointStyle: true,
            color: textColor
          }
        }
      }
    };
  };
  const setStackChartData = () => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'Novenber', 'December'],
      datasets: [
        {
          type: 'bar',
          label: 'Dataset 1',
          backgroundColor: documentStyle.getPropertyValue('--p-cyan-500'),
          data: [50, 25, 12, 48, 90, 76, 42, 22, 11, 34, 80]
        },
        {
          type: 'bar',
          label: 'Dataset 2',
          backgroundColor: documentStyle.getPropertyValue('--p-gray-500'),
          data: [21, 84, 24, 75, 37, 65, 34, 33, 12, 70, 22, 17]
        },
        {
          type: 'bar',
          label: 'Dataset 3',
          backgroundColor: documentStyle.getPropertyValue('--p-orange-500'),
          data: [41, 52, 24, 74, 23, 21, 32, 66, 38, 45, 10, 29]
        }
      ]
    };
  };
  const setStackChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
      maintainAspectRatio: false,
      aspectRatio: 0.8,
      plugins: {
        tooltips: {
          mode: 'index',
          intersect: false
        },
        legend: {
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        },
        y: {
          stacked: true,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        }
      }
    };
  }
  const setPolarChartData = () => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
      datasets: [
        {
          data: [11, 16, 7, 3, 14],
          backgroundColor: [
            documentStyle.getPropertyValue('--p-pink-500'),
            documentStyle.getPropertyValue('--p-gray-500'),
            documentStyle.getPropertyValue('--p-orange-500'),
            documentStyle.getPropertyValue('--p-purple-500'),
            documentStyle.getPropertyValue('--p-cyan-500')
          ],
          label: 'My dataset'
        }
      ],
      labels: ['Pink', 'Gray', 'Orange', 'Purple', 'Cyan']
    };
  };
  const setPolarChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        r: {
          grid: {
            color: surfaceBorder
          }
        }
      }
    };
  }

  const studies = ref([
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YES',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },
    {
      category: 'Residue',
      start_year: 2024,
      task_owner: "Ethan",
      expected_delivery: '2024-10-11',
      registration_typ: 'FEX',
      contract_signed: 'YEX',
      task_progress: 'on going'
    },

  ])

  // console.log(studies.studies)

</script>

<style scoped>

  :deep(.custom-panel) {
    border: 1px solid var(--color-border);
    border-radius: 5px;
    margin-bottom: 20px;
  }

  :deep(.custom-header) {
    background-color: #f1f1f1 !important;
  }

  .dashboard-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .statistics {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-between;
  }

  .card {
    flex: 1;
    display: flex;
    justify-content: center;
    height: 150px;
    border-radius: 5px;
    border: 1px solid var(--p-primary-color);
    padding: 5px;
  }

  .card:hover {
    box-shadow: 0px 0px 5px var(--p-primary-color);
    border: none;
  }
</style>
