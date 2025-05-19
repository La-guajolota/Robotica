// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "custom_msg_svrs/srv/detail/motor_control__struct.h"
#include "custom_msg_svrs/srv/detail/motor_control__type_support.h"
#include "custom_msg_svrs/srv/detail/motor_control__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MotorControl_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MotorControl_Request_type_support_ids_t;

static const _MotorControl_Request_type_support_ids_t _MotorControl_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MotorControl_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MotorControl_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MotorControl_Request_type_support_symbol_names_t _MotorControl_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_svrs, srv, MotorControl_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Request)),
  }
};

typedef struct _MotorControl_Request_type_support_data_t
{
  void * data[2];
} _MotorControl_Request_type_support_data_t;

static _MotorControl_Request_type_support_data_t _MotorControl_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MotorControl_Request_message_typesupport_map = {
  2,
  "custom_msg_svrs",
  &_MotorControl_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MotorControl_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MotorControl_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MotorControl_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MotorControl_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_svrs, srv, MotorControl_Request)() {
  return &::custom_msg_svrs::srv::rosidl_typesupport_c::MotorControl_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__type_support.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MotorControl_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MotorControl_Response_type_support_ids_t;

static const _MotorControl_Response_type_support_ids_t _MotorControl_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MotorControl_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MotorControl_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MotorControl_Response_type_support_symbol_names_t _MotorControl_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_svrs, srv, MotorControl_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Response)),
  }
};

typedef struct _MotorControl_Response_type_support_data_t
{
  void * data[2];
} _MotorControl_Response_type_support_data_t;

static _MotorControl_Response_type_support_data_t _MotorControl_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MotorControl_Response_message_typesupport_map = {
  2,
  "custom_msg_svrs",
  &_MotorControl_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MotorControl_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MotorControl_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MotorControl_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MotorControl_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_svrs, srv, MotorControl_Response)() {
  return &::custom_msg_svrs::srv::rosidl_typesupport_c::MotorControl_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__struct.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__type_support.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _MotorControl_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MotorControl_Event_type_support_ids_t;

static const _MotorControl_Event_type_support_ids_t _MotorControl_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MotorControl_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MotorControl_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MotorControl_Event_type_support_symbol_names_t _MotorControl_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_svrs, srv, MotorControl_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl_Event)),
  }
};

typedef struct _MotorControl_Event_type_support_data_t
{
  void * data[2];
} _MotorControl_Event_type_support_data_t;

static _MotorControl_Event_type_support_data_t _MotorControl_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MotorControl_Event_message_typesupport_map = {
  2,
  "custom_msg_svrs",
  &_MotorControl_Event_message_typesupport_ids.typesupport_identifier[0],
  &_MotorControl_Event_message_typesupport_symbol_names.symbol_name[0],
  &_MotorControl_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MotorControl_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MotorControl_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_hash,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_description,
  &custom_msg_svrs__srv__MotorControl_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_svrs, srv, MotorControl_Event)() {
  return &::custom_msg_svrs::srv::rosidl_typesupport_c::MotorControl_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_msg_svrs/srv/detail/motor_control__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace custom_msg_svrs
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _MotorControl_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MotorControl_type_support_ids_t;

static const _MotorControl_type_support_ids_t _MotorControl_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MotorControl_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MotorControl_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MotorControl_type_support_symbol_names_t _MotorControl_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_svrs, srv, MotorControl)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_svrs, srv, MotorControl)),
  }
};

typedef struct _MotorControl_type_support_data_t
{
  void * data[2];
} _MotorControl_type_support_data_t;

static _MotorControl_type_support_data_t _MotorControl_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MotorControl_service_typesupport_map = {
  2,
  "custom_msg_svrs",
  &_MotorControl_service_typesupport_ids.typesupport_identifier[0],
  &_MotorControl_service_typesupport_symbol_names.symbol_name[0],
  &_MotorControl_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MotorControl_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MotorControl_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &MotorControl_Request_message_type_support_handle,
  &MotorControl_Response_message_type_support_handle,
  &MotorControl_Event_message_type_support_handle,
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

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_svrs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_svrs, srv, MotorControl)() {
  return &::custom_msg_svrs::srv::rosidl_typesupport_c::MotorControl_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
