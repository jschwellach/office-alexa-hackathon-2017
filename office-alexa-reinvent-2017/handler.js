/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills
 * nodejs skill development kit.
 * This sample supports multiple lauguages. (en-US, en-GB, de-DE).
 * The Intent Schema, Custom Slots and Sample Utterances for this skill, as well
 * as testing instructions are located at https://github.com/alexa/skill-sample-nodejs-fact
 **/

'use strict';

const users = {
  'amzn1.ask.account.AFYHQ32LVQ54MEE6B667C4S6FW7NAXQQ6LVZ6SCW5FPSHVZ3IK2G5Y4CU2TW4GGAII7KC2EWB25HOOVBZUZ4SAPKGB6IQFTN3KEGLQCXEQ7DJMMVTDUPFC73JVIUNBHTZYSLTJ6DXNKRMBOCAD76I2GTUUWEV7OO46AGNOC5XBMUBRGSCOWZE6NZZYB5G5CH62DNCQJUHNA7MZA': 'John',
  'amzn1.ask.account.AFYHQ32LVQ54MEE6B667C4S6FW7GCX6TB4F6YKF6Y76SAVLVKARIIKWLKZ4NGTZGEWAE2AGMLDCOM4ZZDCNZ42RWLREYV5LYXUS2D5QRHWC3GAFI44CG3HZYSVTQN5D2RKWRAU4SRXW7ABCSAEFRLTT6LPQP4LQPYER2LFWOEDSBJC5J7AUVJ24BJMZ75VSXSJFCUN557MRJXRQ': 'Tom',
  'amzn1.ask.account.AFW2GRAVB2OG7XBB5AK2G6WTJQWECVWVB5XEFCRTY74RYB3LZBLXPSHQ3MDFMYG6Y4WWTVF4H2H7PBTUMYQXVKAXQWEQ7AA6IVJURWFR7EUD6RJTCJ4XHON5CBDPAXOQHVL4XGKL5RK2QGN6EITCM64ORFULJXKFIMR7V2GU32BWPINCLGVKBSEYAMDUPD7RSCBHGVHSSIDVOGA': 'Tom'
};

const Alexa = require('alexa-sdk');

const APP_ID = "amzn1.ask.skill.42d881a4-20f3-4fe4-897b-3f063403a463";

const languageStrings = {
  'en': {
    translation: {
      FACTS: [
        'A year on Mercury is just 88 days long.',
        'Despite being farther from the Sun, Venus experiences higher temperatures than Mercury.',
        'Venus rotates anti-clockwise, possibly because of a collision in the past with an asteroid.',
        'On Mars, the Sun appears about half the size as it does on Earth.',
        'Earth is the only planet not named after a god.',
        'Jupiter has the shortest day of all the planets.',
        'The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.',
        'The Sun contains 99.86% of the mass in the Solar System.',
        'The Sun is an almost perfect sphere.',
        'A total solar eclipse can happen once every 1 to 2 years. This makes them a rare event.',
        'Saturn radiates two and a half times more energy into space than it receives from the sun.',
        'The temperature inside the Sun can reach 15 million degrees Celsius.',
        'The Moon is moving approximately 3.8 cm away from our planet every year.',
      ],
      SKILL_NAME: 'Space Facts',
      GET_FACT_MESSAGE: "Here's your fact: ",
      HELP_MESSAGE: 'You can say tell me a space fact, or, you can say exit... What can I help you with?',
      HELP_REPROMPT: 'What can I help you with?',
      STOP_MESSAGE: 'Goodbye!',
      CHECK_IN: "I've Checked you in. Have a great day.",
      MEETING_REQUEST: " is asleep at the moment, would you like to try again in 5 hours when it's 9am in John's timezone?",
      MEETING_REQUEST_NOW: " is available now, let me get him on the phone for you."
    },
  },
  'en-US': {
    translation: {
      FACTS: [
        'A year on Mercury is just 88 days long.',
        'Despite being farther from the Sun, Venus experiences higher temperatures than Mercury.',
        'Venus rotates counter-clockwise, possibly because of a collision in the past with an asteroid.',
        'On Mars, the Sun appears about half the size as it does on Earth.',
        'Earth is the only planet not named after a god.',
        'Jupiter has the shortest day of all the planets.',
        'The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.',
        'The Sun contains 99.86% of the mass in the Solar System.',
        'The Sun is an almost perfect sphere.',
        'A total solar eclipse can happen once every 1 to 2 years. This makes them a rare event.',
        'Saturn radiates two and a half times more energy into space than it receives from the sun.',
        'The temperature inside the Sun can reach 15 million degrees Celsius.',
        'The Moon is moving approximately 3.8 cm away from our planet every year.',
      ],
      SKILL_NAME: 'American Space Facts',
    },
  },
  'en-GB': {
    translation: {
      FACTS: [
        'A year on Mercury is just 88 days long.',
        'Despite being farther from the Sun, Venus experiences higher temperatures than Mercury.',
        'Venus rotates anti-clockwise, possibly because of a collision in the past with an asteroid.',
        'On Mars, the Sun appears about half the size as it does on Earth.',
        'Earth is the only planet not named after a god.',
        'Jupiter has the shortest day of all the planets.',
        'The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.',
        'The Sun contains 99.86% of the mass in the Solar System.',
        'The Sun is an almost perfect sphere.',
        'A total solar eclipse can happen once every 1 to 2 years. This makes them a rare event.',
        'Saturn radiates two and a half times more energy into space than it receives from the sun.',
        'The temperature inside the Sun can reach 15 million degrees Celsius.',
        'The Moon is moving approximately 3.8 cm away from our planet every year.',
      ],
      SKILL_NAME: 'British Space Facts',
    },
  },
  'de': {
    translation: {
      FACTS: [
        'Ein Jahr dauert auf dem Merkur nur 88 Tage.',
        'Die Venus ist zwar weiter von der Sonne entfernt, hat aber höhere Temperaturen als Merkur.',
        'Venus dreht sich entgegen dem Uhrzeigersinn, möglicherweise aufgrund eines früheren Zusammenstoßes mit einem Asteroiden.',
        'Auf dem Mars erscheint die Sonne nur halb so groß wie auf der Erde.',
        'Die Erde ist der einzige Planet, der nicht nach einem Gott benannt ist.',
        'Jupiter hat den kürzesten Tag aller Planeten.',
        'Die Milchstraßengalaxis wird in etwa 5 Milliarden Jahren mit der Andromeda-Galaxis zusammenstoßen.',
        'Die Sonne macht rund 99,86 % der Masse im Sonnensystem aus.',
        'Die Sonne ist eine fast perfekte Kugel.',
        'Eine Sonnenfinsternis kann alle ein bis zwei Jahre eintreten. Sie ist daher ein seltenes Ereignis.',
        'Der Saturn strahlt zweieinhalb mal mehr Energie in den Weltraum aus als er von der Sonne erhält.',
        'Die Temperatur in der Sonne kann 15 Millionen Grad Celsius erreichen.',
        'Der Mond entfernt sich von unserem Planeten etwa 3,8 cm pro Jahr.',
      ],
      SKILL_NAME: 'Weltraumwissen auf Deutsch',
      GET_FACT_MESSAGE: 'Hier sind deine Fakten: ',
      HELP_MESSAGE: 'Du kannst sagen, „Nenne mir einen Fakt über den Weltraum“, oder du kannst „Beenden“ sagen... Wie kann ich dir helfen?',
      HELP_REPROMPT: 'Wie kann ich dir helfen?',
      STOP_MESSAGE: 'Auf Wiedersehen!',
    },
  },
};



const handlers = {
  'LaunchRequest': function () {
    this.emit('GetFact');
  },
  'CheckIn': function () {
    const speechOutput = this.t('CHECK_IN');
    console.log('event: ', this.event);
    console.log('user: ', this.event.session.user);
    var user = this.event.session.user;
    var userId = user.userId;
    var userString = users[userId];
    // Save checkin state to dynamo
    this.emit(':tellWithCard', 'Hi ' + userString + ', ' + speechOutput );
  },
  'MeetingRequest': function () {
    // Assuming Tom is the caller
    // John is the target
    var caller = 'Tom';
    var target = 'John';
    console.log('event: ', this.event);
    console.log('user: ', this.event.session.user);
    var user = this.event.session.user;
    var userId = user.userId;
    var userString = users[userId];
    // Save checkin state to dynamo
    const speechOutput = this.t('MEETING_REQUEST');
    this.emit(':tellWithCard', 'Hi ' + userString + ', ' + target + speechOutput);
  },
  'MeetingRequestNow': function () {
    // Assuming Tom is the caller
    // John is the target
    var caller = 'Tom';
    var target = 'John';
    console.log('event: ', this.event);
    console.log('user: ', this.event.session.user);
    var user = this.event.session.user;
    var userId = user.userId;
    var userString = users[userId];
    // Save checkin state to dynamo
    const speechOutput = this.t('MEETING_REQUEST_NOW');
    this.emit(':tellWithCard', 'Hi ' + userString + ', ' + target + speechOutput);
  },
  'GetFact': function () {
    // Get a random space fact from the space facts list
    // Use this.t() to get corresponding language data
    const factArr = this.t('FACTS');
    const factIndex = Math.floor(Math.random() * factArr.length);
    const randomFact = factArr[factIndex];

    // Create speech output
    const speechOutput = this.t('GET_FACT_MESSAGE') + randomFact;
    this.emit(':tellWithCard', speechOutput, this.t('SKILL_NAME'), randomFact);
  },
  'AMAZON.HelpIntent': function () {
    const speechOutput = this.t('HELP_MESSAGE');
    const reprompt = this.t('HELP_MESSAGE');
    this.emit(':ask', speechOutput, reprompt);
  },
  'AMAZON.CancelIntent': function () {
    this.emit(':tell', this.t('STOP_MESSAGE'));
  },
  'AMAZON.StopIntent': function () {
    this.emit(':tell', this.t('STOP_MESSAGE'));
  },
};

exports.handler = function (event, context) {
  const alexa = Alexa.handler(event, context);
  console.log("event:");
  console.log(event);
  console.log("context");
  console.log(context);
  alexa.APP_ID = APP_ID;
  // To enable string internationalization (i18n) features, set a resources object.
  alexa.resources = languageStrings;
  alexa.registerHandlers(handlers);
  alexa.execute();
};
