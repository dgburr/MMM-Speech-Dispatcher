# MMM-Speech-Dispatcher
A MagicMirror² Module for performing Text-to-Speech via speech-dispatcher

## Installation

```sh
$ sudo apt-get install speech-dispatcher python3-speechd
```

Use `spd-confg -u` to configure `speech-dispatcher` to your liking.  At a minimum you will probably have to configure your audio device, e.g.:

```
AudioOutputMethod   libao
```

Use the `spd-say` utility to test that `speech-dispatcher` is configured:

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
