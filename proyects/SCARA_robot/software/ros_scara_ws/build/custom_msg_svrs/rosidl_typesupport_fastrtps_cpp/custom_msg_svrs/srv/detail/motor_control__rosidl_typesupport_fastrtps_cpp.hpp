// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "custom_msg_svrs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "custom_msg_svrs/srv/detail/motor_control__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize(
  const custom_msg_svrs::srv::MotorControl_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  custom_msg_svrs::srv::MotorControl_Request & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size(
  const custom_msg_svrs::srv::MotorControl_Request & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_MotorControl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize_key(
  const custom_msg_svrs::srv::MotorControl_Request & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size_key(
  const custom_msg_svrs::srv::MotorControl_Request & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_key_MotorControl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_msg_svrs, srv, MotorControl_Request)();

#ifdef __cplusplus
}
#endif

// already included above
// #include <cstddef>
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// already included above
// #include "fastcdr/Cdr.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize(
  const custom_msg_svrs::srv::MotorControl_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  custom_msg_svrs::srv::MotorControl_Response & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size(
  const custom_msg_svrs::srv::MotorControl_Response & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_MotorControl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize_key(
  const custom_msg_svrs::srv::MotorControl_Response & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size_key(
  const custom_msg_svrs::srv::MotorControl_Response & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_key_MotorControl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_msg_svrs, srv, MotorControl_Response)();

#ifdef __cplusplus
}
#endif

// already included above
// #include <cstddef>
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// already included above
// #include "fastcdr/Cdr.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize(
  const custom_msg_svrs::srv::MotorControl_Event & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  custom_msg_svrs::srv::MotorControl_Event & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size(
  const custom_msg_svrs::srv::MotorControl_Event & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_MotorControl_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
cdr_serialize_key(
  const custom_msg_svrs::srv::MotorControl_Event & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
get_serialized_size_key(
  const custom_msg_svrs::srv::MotorControl_Event & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
max_serialized_size_key_MotorControl_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_msg_svrs, srv, MotorControl_Event)();

#ifdef __cplusplus
}
#endif

#include "rmw/types.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_msg_svrs
const rosidl_service_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_msg_svrs, srv, MotorControl)();

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
