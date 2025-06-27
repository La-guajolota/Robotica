// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

#include "custom_msg_svrs/srv/detail/motor_control__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_custom_msg_svrs
const rosidl_type_hash_t *
custom_msg_svrs__srv__MotorControl__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xca, 0xfa, 0x38, 0x92, 0x89, 0xc6, 0xbf, 0xa2,
      0xcf, 0x96, 0x41, 0x39, 0xe6, 0x69, 0x45, 0xa7,
      0x50, 0x86, 0xf5, 0x2f, 0x9a, 0x7a, 0x66, 0x91,
      0xd0, 0xb2, 0x31, 0x6c, 0x2f, 0x6f, 0xa9, 0xce,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_msg_svrs
const rosidl_type_hash_t *
custom_msg_svrs__srv__MotorControl_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb1, 0xd7, 0xf9, 0x57, 0x2f, 0x0d, 0x6f, 0xc8,
      0x84, 0xad, 0xd5, 0x3d, 0xfa, 0xa7, 0x63, 0xaf,
      0xd1, 0xa5, 0xe9, 0xd6, 0x98, 0x40, 0x54, 0x82,
      0x64, 0x42, 0xc7, 0x52, 0x20, 0xdc, 0xba, 0xc6,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_msg_svrs
const rosidl_type_hash_t *
custom_msg_svrs__srv__MotorControl_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x5f, 0x65, 0x3b, 0x2d, 0x35, 0x35, 0xa6, 0x3d,
      0xa1, 0x45, 0x90, 0x3c, 0x3a, 0xbd, 0x15, 0x41,
      0x13, 0xa4, 0x24, 0xd5, 0x02, 0x1e, 0x51, 0xfa,
      0x7c, 0x7b, 0x5f, 0x0c, 0xc9, 0x4b, 0x93, 0x89,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_msg_svrs
const rosidl_type_hash_t *
custom_msg_svrs__srv__MotorControl_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x9e, 0xd0, 0x76, 0x40, 0x30, 0xec, 0x57, 0x35,
      0xb2, 0xd9, 0xeb, 0x9c, 0x50, 0xee, 0xfc, 0x07,
      0xf2, 0x9f, 0x24, 0x02, 0x09, 0x20, 0xeb, 0x6c,
      0xf4, 0x79, 0xa6, 0x4d, 0x6c, 0x81, 0x7b, 0x55,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char custom_msg_svrs__srv__MotorControl__TYPE_NAME[] = "custom_msg_svrs/srv/MotorControl";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char custom_msg_svrs__srv__MotorControl_Event__TYPE_NAME[] = "custom_msg_svrs/srv/MotorControl_Event";
static char custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME[] = "custom_msg_svrs/srv/MotorControl_Request";
static char custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME[] = "custom_msg_svrs/srv/MotorControl_Response";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char custom_msg_svrs__srv__MotorControl__FIELD_NAME__request_message[] = "request_message";
static char custom_msg_svrs__srv__MotorControl__FIELD_NAME__response_message[] = "response_message";
static char custom_msg_svrs__srv__MotorControl__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field custom_msg_svrs__srv__MotorControl__FIELDS[] = {
  {
    {custom_msg_svrs__srv__MotorControl__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_msg_svrs__srv__MotorControl_Event__TYPE_NAME, 38, 38},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription custom_msg_svrs__srv__MotorControl__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Event__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_msg_svrs__srv__MotorControl__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_msg_svrs__srv__MotorControl__TYPE_NAME, 32, 32},
      {custom_msg_svrs__srv__MotorControl__FIELDS, 3, 3},
    },
    {custom_msg_svrs__srv__MotorControl__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = custom_msg_svrs__srv__MotorControl_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = custom_msg_svrs__srv__MotorControl_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = custom_msg_svrs__srv__MotorControl_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_uint8[] = "data_uint8";
static char custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_bool[] = "data_bool";
static char custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_float[] = "data_float";

static rosidl_runtime_c__type_description__Field custom_msg_svrs__srv__MotorControl_Request__FIELDS[] = {
  {
    {custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_uint8, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_bool, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Request__FIELD_NAME__data_float, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_msg_svrs__srv__MotorControl_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
      {custom_msg_svrs__srv__MotorControl_Request__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_msg_svrs__srv__MotorControl_Response__FIELD_NAME__response_message[] = "response_message";

static rosidl_runtime_c__type_description__Field custom_msg_svrs__srv__MotorControl_Response__FIELDS[] = {
  {
    {custom_msg_svrs__srv__MotorControl_Response__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_msg_svrs__srv__MotorControl_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
      {custom_msg_svrs__srv__MotorControl_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__info[] = "info";
static char custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__request[] = "request";
static char custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field custom_msg_svrs__srv__MotorControl_Event__FIELDS[] = {
  {
    {custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription custom_msg_svrs__srv__MotorControl_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
  {
    {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_msg_svrs__srv__MotorControl_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_msg_svrs__srv__MotorControl_Event__TYPE_NAME, 38, 38},
      {custom_msg_svrs__srv__MotorControl_Event__FIELDS, 3, 3},
    },
    {custom_msg_svrs__srv__MotorControl_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = custom_msg_svrs__srv__MotorControl_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = custom_msg_svrs__srv__MotorControl_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Request (joint positions)\n"
  "uint8 data_uint8    # which motor\n"
  "bool data_bool      # which direction\n"
  "float32 data_float  # angle to displace\n"
  "---\n"
  "bool response_message # result";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
custom_msg_svrs__srv__MotorControl__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_msg_svrs__srv__MotorControl__TYPE_NAME, 32, 32},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 174, 174},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_msg_svrs__srv__MotorControl_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_msg_svrs__srv__MotorControl_Request__TYPE_NAME, 40, 40},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_msg_svrs__srv__MotorControl_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_msg_svrs__srv__MotorControl_Response__TYPE_NAME, 41, 41},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_msg_svrs__srv__MotorControl_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_msg_svrs__srv__MotorControl_Event__TYPE_NAME, 38, 38},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_msg_svrs__srv__MotorControl__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_msg_svrs__srv__MotorControl__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *custom_msg_svrs__srv__MotorControl_Event__get_individual_type_description_source(NULL);
    sources[3] = *custom_msg_svrs__srv__MotorControl_Request__get_individual_type_description_source(NULL);
    sources[4] = *custom_msg_svrs__srv__MotorControl_Response__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_msg_svrs__srv__MotorControl_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_msg_svrs__srv__MotorControl_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_msg_svrs__srv__MotorControl_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_msg_svrs__srv__MotorControl_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_msg_svrs__srv__MotorControl_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_msg_svrs__srv__MotorControl_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *custom_msg_svrs__srv__MotorControl_Request__get_individual_type_description_source(NULL);
    sources[3] = *custom_msg_svrs__srv__MotorControl_Response__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
