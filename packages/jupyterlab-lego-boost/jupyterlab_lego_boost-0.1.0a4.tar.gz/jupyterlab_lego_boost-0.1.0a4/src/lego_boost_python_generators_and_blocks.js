/*
This extension uses the pylgbst library, which is under the following license:

MIT License

Copyright (c) 2017 Andrey Pokhilko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

var lego_boost_color = '#550a8a';

/*
 * Block definitions
 */

Blockly.Blocks['lego_boost_connect'] = {
  init: function () {
    this.appendValueInput('BLUETOOTH_ADDRESS')
      .setCheck('String')
      .appendField('Connect to MoveHub on address');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Connect to Lego Boost given its Bluetooth address.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_forward'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Move forward for time');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Move motors AB straight forward for a certain time and speed.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_backwards'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Move backwards for time');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Move motors AB straight backwards for a certain time and speed.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_left'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate left');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate left.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_right'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate right');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate right.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_180_left'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate 180° to the left');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate 180° to the left');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_180_right'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate 180° to the right');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate 180° to the right');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_360_left'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate 360° to the left');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate 360° to the left');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_rotate_360_right'] = {
  init: function () {
    this.appendDummyInput().appendField('Rotate 360° to the right');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Rotate 360° to the right');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_turn_right_timed'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Turn right for time');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Turn right for a certain time and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_turn_left_timed'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Turn left for time');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Turn left for a certain time and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_turn_right_angled'] = {
  init: function () {
    this.appendValueInput('ANGLE')
      .setCheck('Number')
      .appendField('Turn right at ');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('angle and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Turn right at a certain angle and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_movement_turn_left_angled'] = {
  init: function () {
    this.appendValueInput('ANGLE')
      .setCheck('Number')
      .appendField('Turn left at ');
    this.appendValueInput('SPEED')
      .setCheck('Number')
      .appendField('angle and with speed');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Turn left at a certain angle and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_move_motor_ab_timed'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Move both motors for time');
    this.appendValueInput('SPEED_A')
      .setCheck('Number')
      .appendField('and speeds for the right motor');
    this.appendValueInput('SPEED_B')
      .setCheck('Number')
      .appendField('and left motor');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Move motors AB for a certain time and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_move_motor_ab_angled'] = {
  init: function () {
    this.appendValueInput('ANGLE')
      .setCheck('Number')
      .appendField('Move both motors at angle');
    this.appendValueInput('SPEED_A')
      .setCheck('Number')
      .appendField('with speeds for right motor');
    this.appendValueInput('SPEED_B')
      .setCheck('Number')
      .appendField('and left motor');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Move group motors AB at a certain angle and speed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_stop_motors'] = {
  init: function () {
    this.appendDummyInput().appendField('Stop motors');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Stop motor.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_disconnect'] = {
  init: function () {
    this.appendDummyInput().appendField('Disconnect from MoveHub');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Disconnect from Lego Boost.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_sleep'] = {
  init: function () {
    this.appendValueInput('SECONDS').setCheck('Number').appendField('Wait for');
    this.appendDummyInput('minutes');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Wait for a given time.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_led_change'] = {
  init: function () {
    this.appendValueInput('COLOR').appendField('Change LED color to');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Change LED color.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_led_off'] = {
  init: function () {
    this.appendDummyInput().appendField('Turn LED off');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Turn LED off.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_led_reset'] = {
  init: function () {
    this.appendDummyInput().appendField('Reset LED');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Reset LED.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_get_current_led_color'] = {
  init: function () {
    this.appendDummyInput().appendField('Get current LED color');
    this.setOutput(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Get current LED color.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_set_led_brightness'] = {
  init: function () {
    this.appendValueInput('BRIGHTNESS')
      .setCheck('Number')
      .appendField('Set LED brightness to');
    this.appendDummyInput().appendField('%');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Set LED brightness procentage. 0% is off, 100% is full brightness.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_color_and_distance'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the color and distance for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the color and distance sensor for detection, for a certain period of time.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_color'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the color for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the color sensor for detection, for a certain period of time.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_distance'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the distance for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the distance sensor for detection, for a certain period of time. Detect the distance until the object placed in front of the robot. The robot can detect a distance from 0 to 10 cm. The number is an integer.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_reflected_distance'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the reflected distance for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the distance sensor for detection, for a certain period of time. Detect the reflected distance until the object placed in front of the robot. The result is a float number from 0 to 1.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_RGB'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the RGB value for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the distance sensor for detection, for a certain period of time. Detect the ambient RGB value of the object placed in front of the robot. '
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_detect_luminosity'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the ambient light value for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Use the distance sensor for detection, for a certain period of time. Detect the ambient light value of the enviroment in front of the robot. The result is a float number from 0 to 1.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_set_sensor_color'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('Set sensor light to color')
      .appendField(
        new Blockly.FieldDropdown([
          ['Red', 'COLOR_RED'],
          ['Blue', 'COLOR_BLUE'],
          ['Cyan', 'COLOR_CYAN'],
          ['Yellow', 'COLOR_YELLOW'],
          ['White', 'COLOR_WHITE'],
          ['Black', 'COLOR_BLACK']
        ]),
        'COLOR'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Set the color of the sensor to one of the selected ones.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_button_state'] = {
  init: function () {
    this.appendDummyInput().appendField('Print the button state');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Output the state of the button. The state is 0 for not pressed and 1 or 2 for pressed.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_position_state_detect'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the 2-axis position state for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Output the postion of the robot according to a 2-axis simple detect.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_position_2axis_angle'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the 2-axis position state in degrees for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Output the postion of the robot according to a 2-axis detect. Returns 2-axis roll and pitch values.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_position_3_axis_state_detect'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the 3-axis position state for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Output the postion of the robot according to a 3-axis simple detect.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_position_3_axis_angle'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the 3-axis position state in degrees for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip(
      'Output the postion of the robot according to a 3-axis detect. Returns 3-axis roll, pitch and yaw values.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['lego_boost_bumps_detect'] = {
  init: function () {
    this.appendValueInput('TIME')
      .setCheck('Number')
      .appendField('Detect the bumps for');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(lego_boost_color);
    this.setTooltip('Detect the bumps.');
    this.setHelpUrl('');
  }
};

/*
 * Generators
 */

pythonGenerator.forBlock['lego_boost_connect'] = function (block) {
  var value_bluetooth_address = pythonGenerator.valueToCode(
    block,
    'BLUETOOTH_ADDRESS',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'conn = get_connection_bleak(hub_mac=' +
    value_bluetooth_address +
    ', hub_name=MoveHub.DEFAULT_NAME)\nhub = MoveHub(conn)\n';
  return code;
};

Blockly.Blocks['lego_boost_connect'].toplevel_init = `
from pylgbst.hub import MoveHub
from pylgbst import get_connection_bleak
import time 

`;

pythonGenerator.forBlock['lego_boost_movement_forward'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_AB.timed(' +
    value_time +
    ', ' +
    value_speed +
    ', ' +
    value_speed +
    ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_backwards'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_AB.timed( ' +
    value_time +
    ', -' +
    value_speed +
    ', -' +
    value_speed +
    ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_right'] = function (
  block
) {
  var code = 'hub.motor_A.angled(540, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_left'] = function (block) {
  var code = 'hub.motor_B.angled(540, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_180_left'] = function (
  block
) {
  var code = 'hub.motor_B.angled(1080, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_180_right'] = function (
  block
) {
  var code = 'hub.motor_A.angled(1080, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_360_left'] = function (
  block
) {
  var code = 'hub.motor_B.timed(1.7, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_rotate_360_right'] = function (
  block
) {
  var code = 'hub.motor_A.timed(1.7, 1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_turn_right_timed'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code = 'hub.motor_A.timed(' + value_time + ', ' + value_speed + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_turn_left_timed'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code = 'hub.motor_B.timed(' + value_time + ', ' + value_speed + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_turn_right_angled'] = function (
  block
) {
  var value_angle = pythonGenerator.valueToCode(
    block,
    'ANGLE',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_A.angled(' + value_angle * 6 + ', ' + value_speed + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_movement_turn_left_angled'] = function (
  block
) {
  var value_angle = pythonGenerator.valueToCode(
    block,
    'ANGLE',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_B.angled(' + value_angle * 6 + ', ' + value_speed + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_move_motor_ab_timed'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed_a = pythonGenerator.valueToCode(
    block,
    'SPEED_A',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed_b = pythonGenerator.valueToCode(
    block,
    'SPEED_B',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_AB.timed(' +
    value_time +
    ', ' +
    value_speed_a +
    ', ' +
    value_speed_b +
    ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_move_motor_ab_angled'] = function (block) {
  var value_angle = pythonGenerator.valueToCode(
    block,
    'ANGLE',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed_a = pythonGenerator.valueToCode(
    block,
    'SPEED_A',
    pythonGenerator.ORDER_ATOMIC
  );

  var value_speed_b = pythonGenerator.valueToCode(
    block,
    'SPEED_B',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'hub.motor_AB.angled(' +
    value_angle +
    ', ' +
    value_speed_a * ', ' +
    value_speed_b +
    ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_start_speed'] = function (block) {
  var value_speed = pythonGenerator.valueToCode(
    block,
    'SPEED',
    pythonGenerator.ORDER_ATOMIC
  );

  var code = 'hub.motor_external.start_speed(' + value_speed + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_stop_motors'] = function (block) {
  var code = 'hub.motor_external.stop()\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_disconnect'] = function (block) {
  var code = 'hub.disconnect()\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_sleep'] = function (block) {
  var value_seconds = pythonGenerator.valueToCode(
    block,
    'SECONDS',
    pythonGenerator.ORDER_ATOMIC
  );

  var code = 'time.sleep(' + value_seconds + ')\n';
  return code;
};

Blockly.Blocks['lego_boost_led_change'].toplevel_init = `
def hex_to_rgb(value):
    value = value.lstrip('#')
    return (tuple(int(value[i:i+2], 16) for i in (0, 2, 4)))

`;

pythonGenerator.forBlock['lego_boost_led_change'] = function (block) {
  var value_color = pythonGenerator.valueToCode(
    block,
    'COLOR',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'color = hex_to_rgb(' + value_color + ')\nhub.led.set_color(color)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_led_off'] = function (block) {
  var code = 'hub.led.set_color((0, 0, 0))\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_led_reset'] = function (block) {
  var code =
    "if hub != 'None':\n  hub.led.set_color((0, 0, 255))\nelse:\n  hub.led.set_color(0, 0, 0)\n";
  return code;
};

Blockly.Blocks['lego_boost_get_current_led_color'].toplevel_init = `
from pylgbst.peripherals import LEDRGB
`;

pythonGenerator.forBlock['lego_boost_get_current_led_color'] = function (
  block
) {
  var code = 'hub.led.get_sensor_data(LEDRGB.MODE_RGB)\n';
  return [code, pythonGenerator.ORDER_NONE];
};

pythonGenerator.forBlock['lego_boost_set_led_brightness'] = function (block) {
  var value_brightness = pythonGenerator.valueToCode(
    block,
    'BRIGHTNESS',
    pythonGenerator.ORDER_ATOMIC
  );

  var code = 'hub.port_LED.set_brightness(' + value_brightness + ')\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_color_and_distance'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_color_and_distance'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(color, distance):\n    print("Color: %s / Distance: %s" % (color, distance))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_color'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_color'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(color):\n    print("Color: %s" % (color))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_INDEX)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_distance'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_distance'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(distance):\n    print("Distance: %s" % (distance))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.DISTANCE_INCHES)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_reflected_distance'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_reflected_distance'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(reflected):\n    print("Reflected distance: %s" % (reflected))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.DISTANCE_REFLECTED)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_luminosity'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_luminosity'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(luminosity):\n    print("Ambient light: %s" % (luminosity))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.AMBIENT_LIGHT)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_detect_RGB'].toplevel_init = `
from pylgbst.hub import VisionSensor

`;

pythonGenerator.forBlock['lego_boost_detect_RGB'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(red, green, blue):\n    print("Color RGB: %s" % (red, green, blue))\nhub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_RGB)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.vision_sensor.unsubscribe(callback)\n';
  return code;
};

Blockly.Blocks['lego_boost_set_sensor_color'].toplevel_init = `
from pylgbst.hub import VisionSensor, COLOR_BLUE, COLOR_CYAN, COLOR_YELLOW, COLOR_RED, COLOR_WHITE, COLOR_BLACK

`;

pythonGenerator.forBlock['lego_boost_set_sensor_color'] = function (block) {
  var dropdown_color_value = block.getFieldValue('COLOR');
  var code = 'hub.vision_sensor.set_color(' + dropdown_color_value + ')\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_button_state'] = function (block) {
  var code =
    'def callback(is_pressed):\n    print("Btn pressed: %s" % is_pressed)\nhub.button.subscribe(callback)\ntime.sleep(1)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_position_state_detect'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(state):\n    print("2-axis state: %s" % (state))\nhub.tilt_sensor.subscribe(callback, mode=TiltSensor.MODE_2AXIS_SIMPLE)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.tilt_sensor.unsubscribe(callback)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_position_2axis_angle'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(roll, pitch):\n    print("Roll: %s / Pitch: %s" % (roll, pitch))\nhub.tilt_sensor.subscribe(callback, mode=TiltSensor.MODE_2AXIS_ANGLE)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.tilt_sensor.unsubscribe(callback)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_position_3_axis_state_detect'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(state):\n    print("3-axis state: %s" % (state))\nhub.tilt_sensor.subscribe(callback, mode=TiltSensor.MODE_3AXIS_SIMPLE)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.tilt_sensor.unsubscribe(callback)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_position_3_axis_angle'] = function (
  block
) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(roll, pitch, yaw):\n    print("Roll: %s / Pitch: %s / Yaw: %s" % (roll, pitch, yaw))\nhub.tilt_sensor.subscribe(callback, mode=TiltSensor.MODE_2AXIS_ACCEL)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.tilt_sensor.unsubscribe(callback)\n';
  return code;
};

pythonGenerator.forBlock['lego_boost_bumps_detect'] = function (block) {
  var value_time = pythonGenerator.valueToCode(
    block,
    'TIME',
    pythonGenerator.ORDER_ATOMIC
  );

  var code =
    'def callback(state):\n    print("Bumps state: %s" % (state))\nhub.tilt_sensor.subscribe(callback, mode=TiltSensor.MODE_IMPACT_COUNT)\ntime.sleep(' +
    value_time +
    ')# play with sensor while it waits\nhub.tilt_sensor.unsubscribe(callback)\n';
  return code;
};

// Creating a toolbox containing all the main blocks
// and adding the lego boost catgory.
const TOOLBOX = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'category',
      name: 'Logic',
      colour: '210',
      contents: [
        {
          kind: 'block',
          type: 'controls_if'
        },
        {
          kind: 'BLOCK',
          type: 'logic_compare'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_operation"></block>',
          type: 'logic_operation'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_negate"></block>',
          type: 'logic_negate'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_boolean"></block>',
          type: 'logic_boolean'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_null"></block>',
          type: 'logic_null'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_ternary"></block>',
          type: 'logic_ternary'
        }
      ]
    },
    {
      kind: 'category',
      name: 'Loops',
      colour: '120',
      contents: [
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'controls_repeat_ext'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_whileUntil"></block>',
          type: 'controls_whileUntil'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'controls_for'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_forEach"></block>',
          type: 'controls_forEach'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_flow_statements"></block>',
          type: 'controls_flow_statements'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Math',
      colour: '230',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_number"></block>',
          type: 'math_number'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_arithmetic'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_single'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_trig'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_constant"></block>',
          type: 'math_constant'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_number_property'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_change'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_round'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_on_list"></block>',
          type: 'math_on_list'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_modulo'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_constrain'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_random_int'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_random_float"></block>',
          type: 'math_random_float'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Text',
      colour: '160',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="text"></block>',
          type: 'text'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="text_join"></block>',
          type: 'text_join'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
          type: 'text_append'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_length'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_isEmpty'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_indexOf'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
          type: 'text_charAt'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
          type: 'text_getSubstring'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_changeCase'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_trim'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_print'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_prompt_ext'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Lists',
      colour: '260',
      contents: [
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
          type: 'lists_create_with'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_create_with"></block>',
          type: 'lists_create_with'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'lists_repeat'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_length"></block>',
          type: 'lists_length'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_isEmpty"></block>',
          type: 'lists_isEmpty'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_indexOf'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_getIndex'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_setIndex'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_getSublist'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'lists_split'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_sort"></block>',
          type: 'lists_sort'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Color',
      colour: '20',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="colour_picker"></block>',
          type: 'colour_picker'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="colour_random"></block>',
          type: 'colour_random'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'colour_rgb'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'colour_blend'
        }
      ]
    },
    {
      kind: 'SEP'
    },
    {
      kind: 'CATEGORY',
      colour: '330',
      custom: 'VARIABLE',
      name: 'Variables'
    },
    {
      kind: 'CATEGORY',
      colour: '290',
      custom: 'PROCEDURE',
      name: 'Functions'
    },
    {
      kind: 'SEP'
    },
    {
      kind: 'CATEGORY',
      colour: lego_boost_color,
      name: 'Lego Boost',
      contents: [
        {
          kind: 'BLOCK',
          type: 'lego_boost_connect'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_forward'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_backwards'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_left'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_right'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_180_left'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_180_right'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_360_left'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_rotate_360_right'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_turn_left_timed'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_turn_right_timed'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_turn_left_angled'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_movement_turn_right_angled'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_move_motor_ab_timed'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_move_motor_ab_angled'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_stop_motors'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_disconnect'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_sleep'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_led_change'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_led_off'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_led_reset'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_get_current_led_color'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_color_and_distance'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_color'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_distance'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_reflected_distance'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_luminosity'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_detect_RGB'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_set_sensor_color'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_button_state'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_position_state_detect'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_position_2axis_angle'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_position_3_axis_state_detect'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_position_3_axis_angle'
        },
        {
          kind: 'BLOCK',
          type: 'lego_boost_bumps_detect'
        }
        // {
        //   kind: 'BLOCK',
        //   type: 'lego_boost_set_led_brightness'
        // }
      ]
    }
  ]
};

const BlocklyBoost = {
  Blocks: Blockly.Blocks,
  Generator: pythonGenerator,
  Toolbox: TOOLBOX
};

export default BlocklyBoost;
