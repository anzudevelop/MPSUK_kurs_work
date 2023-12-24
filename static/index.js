const postData = async(url, data = {}) => {
    const response = await axios
    .post(url, data)
    .catch(error => console.error(error))
    return response.data
}
const getData = async(url) => {
    const response = await axios
    .get(url)
    .catch(error => console.error(error))
    return response.data
}


// async function setGpioState(pin, state) {
//     await postData(`/setGpioState`, {pin: pin, state: state})
// }

async function getLogs() {
    const response = await getData(`/logs`)
    return response
}
async function getChartData() {
    const response = await getData(`/get_histogram`)
    return response
}
async function setNewRange(newRange) {
    if(Number(newRange) < 0 || Number(newRange) > 127) {
        alert("Значение должно находиться в диапазоне от 0 до 100")
        return
    }
    await postData('setRange', {range: newRange})
}

const app = new Vue({
    el: "#app",
    data: {
        imageSrc: '',
        logsLine: "",
        loadInfo: false,
        range: 0,
    },
    mounted() {
        /*getLogs().then(response => this.logsLine = `pwm = ${response}`)
        setInterval(() => {
            getLogs().then(response => this.logsLine = `pwm = ${response}`)
        }, 3000)*/
    },
    methods: {
        btnClick: async function() {
            this.loadInfo = true
            this.imageSrc = '',
            this.logsLine = "",
            document.getElementById("containerChart").innerHTML = ""
            await fetch("/get_image")
            .then(response => response.blob())
            .then(data => {
                this.imageSrc = URL.createObjectURL(data)
            })
            this.loadInfo = false
            await getChartData().then(response => {
                let data = []
                for(let i = 0; i < response.length; i++) {
                    data.push({x: i, value: response[i]})
                }
                var chart = anychart.line(data);
                chart.xAxis().title("Яркость(0-255)");
                chart.yAxis().title("Пикселей, %");
                //chart.yScale().maximum(100);
                chart.title("Гистрограмма");
                chart.container("containerChart").draw();
            })
            await getLogs().then(response => this.logsLine = `Значение шим = ${response}%`)
        },
        btnChangeRangeClick: function() {
            setNewRange(this.range)
        },
    },
})