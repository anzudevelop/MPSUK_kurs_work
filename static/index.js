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

async function getGpioState(pin) {
    const response = await getData(`/getGpioState?pin=${pin}`)
    return response
}
async function setGpioState(pin, state) {
    await postData(`/setGpioState`, {pin: pin, state: state})
}

const app = new Vue({
    el: "#app",
    data: {
        imageSrc: '../img/image.jpg'
    },
    mounted() {
        //this.updateState()
    },
    methods: {
        sendStringToFile: function() {
            console.log(this.stringToFile)
            postData('/setStringToFile', {text: this.stringToFile})
            this.stringToFile = ''
        },
        onBtnClick: function() {
            setGpioState(40, 'on')
            .then(() => {
                this.updateState()
            })
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