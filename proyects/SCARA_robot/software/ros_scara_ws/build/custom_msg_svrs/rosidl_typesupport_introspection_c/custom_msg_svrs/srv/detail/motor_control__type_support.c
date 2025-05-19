// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "custom_msg_svrs/srv/detail/motor_control__rosidl_typesupport_introspection_c.h"
#include "custom_msg_svrs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "custom_msg_svrs/srv/detail/motor_control__functions.h"
#include "custom_msg_svrs/srv/detail/motor_control__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_msg_svrs__srv__MotorControl_Request__init(message_memory);
}

void custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_fini_function(void * message_memory)
{
  custom_msg_svrs__srv__MotorControl_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_member_array[3] = {
  {
    "data_uint8",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Request, data_uint8),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data_bool",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Request, data_bool),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data_float",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Request, data_float),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_members = {
  "custom_msg_svrs__srv",  // message namespace
  "MotorControl_Request",  // message name
  3,  // number of fields
  sizeof(custom_msg_svrs__srv__MotorControl_Request),
  false,  // has_any_key_member_
  custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_member_array,  // message members
  custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle = {
  0,
  &custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_members,
  get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_msg_svrs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Request)() {
  if (!custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle.typesupport_identifier) {
    custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__rosidl_typesupport_introspection_c.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__functions.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.h"


// Include directives for member types
// Member `response_message`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_msg_svrs__srv__MotorControl_Response__init(message_memory);
}

void custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_fini_function(void * message_memory)
{
  custom_msg_svrs__srv__MotorControl_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_member_array[1] = {
  {
    "response_message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Response, response_message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_members = {
  "custom_msg_svrs__srv",  // message namespace
  "MotorControl_Response",  // message name
  1,  // number of fields
  sizeof(custom_msg_svrs__srv__MotorControl_Response),
  false,  // has_any_key_member_
  custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_member_array,  // message members
  custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle = {
  0,
  &custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_members,
  get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_msg_svrs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Response)() {
  if (!custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle.typesupport_identifier) {
    custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__rosidl_typesupport_introspection_c.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__functions.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "custom_msg_svrs/srv/motor_control.h"
// Member `request`
// Member `response`
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_msg_svrs__srv__MotorControl_Event__init(message_memory);
}

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_fini_function(void * message_memory)
{
  custom_msg_svrs__srv__MotorControl_Event__fini(message_memory);
}

size_t custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__size_function__MotorControl_Event__request(
  const void * untyped_member)
{
  const custom_msg_svrs__srv__MotorControl_Request__Sequence * member =
    (const custom_msg_svrs__srv__MotorControl_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__request(
  const void * untyped_member, size_t index)
{
  const custom_msg_svrs__srv__MotorControl_Request__Sequence * member =
    (const custom_msg_svrs__srv__MotorControl_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__request(
  void * untyped_member, size_t index)
{
  custom_msg_svrs__srv__MotorControl_Request__Sequence * member =
    (custom_msg_svrs__srv__MotorControl_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__fetch_function__MotorControl_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const custom_msg_svrs__srv__MotorControl_Request * item =
    ((const custom_msg_svrs__srv__MotorControl_Request *)
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__request(untyped_member, index));
  custom_msg_svrs__srv__MotorControl_Request * value =
    (custom_msg_svrs__srv__MotorControl_Request *)(untyped_value);
  *value = *item;
}

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__assign_function__MotorControl_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  custom_msg_svrs__srv__MotorControl_Request * item =
    ((custom_msg_svrs__srv__MotorControl_Request *)
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__request(untyped_member, index));
  const custom_msg_svrs__srv__MotorControl_Request * value =
    (const custom_msg_svrs__srv__MotorControl_Request *)(untyped_value);
  *item = *value;
}

bool custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__resize_function__MotorControl_Event__request(
  void * untyped_member, size_t size)
{
  custom_msg_svrs__srv__MotorControl_Request__Sequence * member =
    (custom_msg_svrs__srv__MotorControl_Request__Sequence *)(untyped_member);
  custom_msg_svrs__srv__MotorControl_Request__Sequence__fini(member);
  return custom_msg_svrs__srv__MotorControl_Request__Sequence__init(member, size);
}

size_t custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__size_function__MotorControl_Event__response(
  const void * untyped_member)
{
  const custom_msg_svrs__srv__MotorControl_Response__Sequence * member =
    (const custom_msg_svrs__srv__MotorControl_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__response(
  const void * untyped_member, size_t index)
{
  const custom_msg_svrs__srv__MotorControl_Response__Sequence * member =
    (const custom_msg_svrs__srv__MotorControl_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__response(
  void * untyped_member, size_t index)
{
  custom_msg_svrs__srv__MotorControl_Response__Sequence * member =
    (custom_msg_svrs__srv__MotorControl_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__fetch_function__MotorControl_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const custom_msg_svrs__srv__MotorControl_Response * item =
    ((const custom_msg_svrs__srv__MotorControl_Response *)
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__response(untyped_member, index));
  custom_msg_svrs__srv__MotorControl_Response * value =
    (custom_msg_svrs__srv__MotorControl_Response *)(untyped_value);
  *value = *item;
}

void custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__assign_function__MotorControl_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  custom_msg_svrs__srv__MotorControl_Response * item =
    ((custom_msg_svrs__srv__MotorControl_Response *)
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__response(untyped_member, index));
  const custom_msg_svrs__srv__MotorControl_Response * value =
    (const custom_msg_svrs__srv__MotorControl_Response *)(untyped_value);
  *item = *value;
}

bool custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__resize_function__MotorControl_Event__response(
  void * untyped_member, size_t size)
{
  custom_msg_svrs__srv__MotorControl_Response__Sequence * member =
    (custom_msg_svrs__srv__MotorControl_Response__Sequence *)(untyped_member);
  custom_msg_svrs__srv__MotorControl_Response__Sequence__fini(member);
  return custom_msg_svrs__srv__MotorControl_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Event, request),  // bytes offset in struct
    NULL,  // default value
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__size_function__MotorControl_Event__request,  // size() function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__request,  // get_const(index) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__request,  // get(index) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__fetch_function__MotorControl_Event__request,  // fetch(index, &value) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__assign_function__MotorControl_Event__request,  // assign(index, value) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__resize_function__MotorControl_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(custom_msg_svrs__srv__MotorControl_Event, response),  // bytes offset in struct
    NULL,  // default value
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__size_function__MotorControl_Event__response,  // size() function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_const_function__MotorControl_Event__response,  // get_const(index) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__get_function__MotorControl_Event__response,  // get(index) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__fetch_function__MotorControl_Event__response,  // fetch(index, &value) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__assign_function__MotorControl_Event__response,  // assign(index, value) function pointer
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__resize_function__MotorControl_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_members = {
  "custom_msg_svrs__srv",  // message namespace
  "MotorControl_Event",  // message name
  3,  // number of fields
  sizeof(custom_msg_svrs__srv__MotorControl_Event),
  false,  // has_any_key_member_
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_member_array,  // message members
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_type_support_handle = {
  0,
  &custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_members,
  get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_msg_svrs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Event)() {
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Request)();
  custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Response)();
  if (!custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_type_support_handle.typesupport_identifier) {
    custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_msg_svrs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_members = {
  "custom_msg_svrs__srv",  // service namespace
  "MotorControl",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle,
  NULL,  // response message
  // custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle
  NULL  // event_message
  // custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle
};


static rosidl_service_type_support_t custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_type_support_handle = {
  0,
  &custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_members,
  get_service_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Request__rosidl_typesupport_introspection_c__MotorControl_Request_message_type_support_handle,
  &custom_msg_svrs__srv__MotorControl_Response__rosidl_typesupport_introspection_c__MotorControl_Response_message_type_support_handle,
  &custom_msg_svrs__srv__MotorControl_Event__rosidl_typesupport_introspection_c__MotorControl_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    custom_msg_svrs,
    srv,
    MotorControl
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    custom_msg_svrs,
    srv,
    MotorControl
  ),
  &custom_msg_svrs__srv__MotorControl__get_type_hash,
  &custom_msg_svrs__srv__MotorControl__get_type_description,
  &custom_msg_svrs__srv__MotorControl__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_msg_svrs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl)(void) {
  if (!custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_type_support_handle.typesupport_identifier) {
    custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Event)()->data;
  }

  return &custom_msg_svrs__srv__detail__motor_control__rosidl_typesupport_introspection_c__MotorControl_service_type_support_handle;
}
