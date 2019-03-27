# MMM-Speech-Dispatcher
A MagicMirror² Module for performing Text-to-Speech via speech-dispatcher

## Installation

Install `speech-dispatcher` and python bindings:

```sh
$ sudo apt-get install speech-dispatcher python3-speechd
```

Install output plug-ins for `speech-dispatcher`, e.g.:

```sh
$ sudo apt-get install speech-dispatcher-audio-plugins speech-dispatcher-espeak-ng libttspico-utils
```

Use `spd-confg -u` to configure `speech-dispatcher` to your liking.  At a minimum you will probably have to configure your audio device, e.g.:

```
AudioOutputMethod   libao
```

Use the `spd-say` utility to test that `speech-dispatcher` is configured, e.g.:

```sh
$ spd-say "Hello World!"
```

## Configuration

Default configuration:

```javascript
{
    module: "MMM-Speech-Dispatcher",
    config: {
        module: null,   // output module, e.g. "espeak-ng", "festival" or "pico-generic"
        voice: null,    // voice to use, e.g. "english_rp en gb-x-r" or "female2"
        language: null, // two letter language code, e.g. "en"
        rate: null,     // speaking rate [-100-100]
        notification: "SPEECH_DISPATCHER_SAID", // notification to send after text has been spoken
    }
}
```

Example configuration for use with `MMM-PageReader`:

```javascript
{
    module: "MMM-Speech-Dispatcher",
    config: {
        module: "pico-generic",
        voice: "female2",
        notification: "PAGE_READ_NEXT",
    }
}
```

## Notifications
Upon reception of a `SPEECH_DISPATCHER_SAY` notification, `MMM-Speech-Dispatcher` will send the payload text to `speech-dispatcher`.  If the `notification` option has been specified in the configuration then `MMM-Speech-Dispatcher` will send an outgoing notification of that type when speaking is complete (default value is `SPEECH_DISPATCHER_SAID`).
