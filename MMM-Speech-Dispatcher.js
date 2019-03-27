/*
 * File:        MMM-Speech-Dispatcher.js
 * Created:     27/03/2019 by Daniel Burr <dburr@dburr.net>
 * Description: Main file for MMM-Speech-Dispatcher
 * License:     GNU Public License, version 3
 */

Module.register('MMM-Speech-Dispatcher', {
    defaults: {
        module: null,   // output module, e.g. "espeak-ng", "festival" or "pico-generic"
        voice: null,    // voice to use, e.g. "english_rp en gb-x-r" or "female2"
        language: null, // two letter language code, e.g. "en"
        rate: null,     // speaking rate [-100-100]
        notification: "SPEECH_DISPATCHER_SAID", // notification to send after text has been spoken
    },

    start() {
        Log.info(`Starting module: ${this.name}`)
        this.sendSocketNotification('CONFIG', this.config)
    },

    notificationReceived(notification, payload) {
        if(notification === 'SPEECH_DISPATCHER_SAY') {
            var text = payload.replace("&nbsp;", ' ')
            text = text.replace(/\s+/gm, ' ')) // strip newlines
            this.sendSocketNotification('TTS', text)
        }
    },

    socketNotificationReceived(notification) {
        if(notification === 'FINISHED') {
            if(this.config.notification) this.sendNotification(this.config.notification)
        }
    },

    getDom: function() {
        return document.createElement("div")
    },

});
