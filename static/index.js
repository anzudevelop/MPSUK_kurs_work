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

const app = new Vue({
    el: "#app",
    data: {
        imageSrc: '',
        logsLine: "",
    },
    mounted() {
        getLogs().then(response => this.logsLine = `pwm = ${response}`)
        setInterval(() => {
            getLogs().then(response => this.logsLine = `pwm = ${response}`)
        }, 3000)
        //this.updateState()
    },
    methods: {
        btnClick: function() {
            fetch("/get_image")
            .then(response => response.blob())
            .then(data => {
                this.imageSrc = URL.createObjectURL(data)
            });
        },

        sendStringToFile: function() {
            console.log(this.stringToFile)
            postData('/setStringToFile', {text: this.stringToFile})
            this.stringToFile = ''
        },
        offBtnClick: function() {
            setGpioState(40, 'off')
            .then(() => {
                this.updateState()
            })
        },
        updateState: function() {
            getGpioState(40)
            .then(state => {
                this.state = state
                this.stateLedImg = (state == 'on') ? "./static/ledOn.png" : "./static/ledOff.png"
            })
        },
    },
})