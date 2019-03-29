/*
 * File:        node_helper.js
 * Created:     27/03/2019 by Daniel Burr <dburr@dburr.net>
 * Description: Node helper for MMM-Speech-Dispatcher
 */

const NodeHelper = require('node_helper');
const spawn = require('child_process').spawn;

module.exports = NodeHelper.create({

    start() {
        console.log(`Starting node helper for: ${this.name}`);
        this.speakProcess = null
    },

    socketNotificationReceived(notification, payload) {
        if(notification === 'CONFIG') {
            this.config = payload;
            this.startSpeechDispatcher()
        } else if(notification === 'TTS') {
            if(this.speakProcess) {
                this.speakProcess.stdin.write(payload + "\n");
            }
        }
    },

    startSpeechDispatcher() {
        var self = this;

        var script = './modules/MMM-Speech-Dispatcher/ssip_client.py'
        var params = []
        if(this.config.voice) params.push("--voice=" + this.config.voice)
        if(this.config.rate) params.push("--rate=" + this.config.rate)
        if(this.config.language) params.push("--language=" + this.config.language)
        if(this.config.module) params.push("--module=" + this.config.module)

        console.log("Starting speech-dispatcher: " + script + " " + params)

        this.speakProcess = spawn(script, params, { detached: false })
        this.speakProcess.stdout.on('data', function (data) {
            var message = data.toString()
            if(message.startsWith('FINISHED_UTTERANCE')) {
                self.sendSocketNotification("FINISHED")
            } else {
                console.error(message)
            }
        })
        this.speakProcess.stderr.on('data', function (data) {
            console.log(data.toString())
        })
    },
});
