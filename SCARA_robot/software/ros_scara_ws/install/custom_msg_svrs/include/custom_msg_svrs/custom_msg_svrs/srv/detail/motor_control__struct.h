// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_msg_svrs/srv/motor_control.h"


#ifndef CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_H_
#define CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MotorControl in the package custom_msg_svrs.
typedef struct custom_msg_svrs__srv__MotorControl_Request
{
  /// which motor
  uint8_t data_uint8;
  /// which direction
  bool data_bool;
  /// angle to displace
  float data_float;
} custom_msg_svrs__srv__MotorControl_Request;

// Struct for a sequence of custom_msg_svrs__srv__MotorControl_Request.
typedef struct custom_msg_svrs__srv__MotorControl_Request__Sequence
{
  custom_msg_svrs__srv__MotorControl_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_svrs__srv__MotorControl_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'response_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MotorControl in the package custom_msg_svrs.
typedef struct custom_msg_svrs__srv__MotorControl_Response
{
  /// result
  rosidl_runtime_c__String response_message;
} custom_msg_svrs__srv__MotorControl_Response;

// Struct for a sequence of custom_msg_svrs__srv__MotorControl_Response.
typedef struct custom_msg_svrs__srv__MotorControl_Response__Sequence
{
  custom_msg_svrs__srv__MotorControl_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_svrs__srv__MotorControl_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  custom_msg_svrs__srv__MotorControl_Event__request__MAX_SIZE = 1
};
// response
enum
{
  custom_msg_svrs__srv__MotorControl_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/MotorControl in the package custom_msg_svrs.
typedef struct custom_msg_svrs__srv__MotorControl_Event
{
  service_msgs__msg__ServiceEventInfo info;
  custom_msg_svrs__srv__MotorControl_Request__Sequence request;
  custom_msg_svrs__srv__MotorControl_Response__Sequence response;
} custom_msg_svrs__srv__MotorControl_Event;

// Struct for a sequence of custom_msg_svrs__srv__MotorControl_Event.
typedef struct custom_msg_svrs__srv__MotorControl_Event__Sequence
{
  custom_msg_svrs__srv__MotorControl_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_svrs__srv__MotorControl_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_H_
