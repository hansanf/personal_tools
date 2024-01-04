# PG_PROTO_DIR: the import path for proto files
# PC_PROTOBUF_PREFIX: "${protobuf_SOURCE_DIR}"
# PG_GENERATED_DIR: set proto.pb.h/cc path
################################################################################
########################## define functions ####################################
function(_find_protobuf_compiler)
    set(PROTOBUF_COMPILER_CANDIDATES "${PC_PROTOBUF_PREFIX}/bin/protoc")
    foreach (candidate ${PROTOBUF_COMPILER_CANDIDATES})
        if (EXISTS ${candidate})
            set(PROTOBUF_COMPILER ${candidate} PARENT_SCOPE)
            return()
        endif ()
    endforeach ()
    message(FATAL_ERROR "PROTOBUF_COMPILER_CANDIDATES:" ${PROTOBUF_COMPILER_CANDIDATES})
    message(FATAL_ERROR "Couldn't find protobuf compiler. Please ensure that protobuf(>=3.3.0 version) is properly installed to /usr/local from source. Checked the following paths: ${PROTOBUF_COMPILER_CANDIDATES}")
endfunction()


# ====================  PG_PROTOBUF_GENERATE_CPP  ==========================
function(PG_PROTOBUF_GENERATE_CPP SRCS HDRS)
    if (NOT ARGN)
        message(SEND_ERROR "Error: PG_PROTOBUF_GENERATE_CPP() called without any proto files")
        return()
    endif ()

    if (PROTOBUF_GENERATE_CPP_APPEND_PATH)
        # Create an include path for each file specified
        message(STATUS "PROTOBUF_GENERATE_CPP_APPEND_PATH: TRUE")
        foreach (FIL ${ARGN})
            get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
            get_filename_component(ABS_PATH ${ABS_FIL} PATH)
            list(FIND _protobuf_include_path ${ABS_PATH} _contains_already)
            if (${_contains_already} EQUAL -1)
                list(APPEND _protobuf_include_path -I ${ABS_PATH})
            endif ()
        endforeach ()
    else ()
        # assume all .proto are in project_name/proto folder
        set(_protobuf_include_path -I ${CMAKE_CURRENT_SOURCE_DIR}/proto)
    endif ()
    # create project folder devel/include/project_name/proto
    # Folder where the generated headers are installed to. This should resolve to
    # devel/include/project_name/proto

    list(APPEND _protobuf_include_path -I ${CMAKE_CURRENT_SOURCE_DIR})


    set(${SRCS})
    set(${HDRS})
    _find_protobuf_compiler()
    foreach (FIL ${ARGN})
        get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
        get_filename_component(FIL_WE ${FIL} NAME_WE)
        get_filename_component(RELT_DIR ${FIL} DIRECTORY)
        # generated the same directory structure for proto files
        set(GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}")

        message(STATUS "GENERATED_DIR:" ${GENERATED_DIR})

        set(GENERATED_SRC "${GENERATED_DIR}/${FIL_WE}.pb.cc")
        set(GENERATED_HDR "${GENERATED_DIR}/${FIL_WE}.pb.h")
        message(STATUS "GENERATED_SRC:" ${GENERATED_SRC})
        message(STATUS "GENERATED_HDR:" ${GENERATED_HDR})
        message(STATUS "PG_PROTO_DIR:" ${PG_PROTO_DIR})

        list(APPEND ${SRCS} "${GENERATED_SRC}")
        list(APPEND ${HDRS} "${GENERATED_HDR}")
        # set PG_PROTO_DIR
        add_custom_command(
                OUTPUT ${GENERATED_SRC} ${GENERATED_HDR}
                COMMAND ${PROTOBUF_COMPILER} --proto_path=${PG_PROTO_DIR} --cpp_out=${PG_GENERATED_DIR} ${ABS_FIL}
                DEPENDS ${ABS_FIL} ${PROTOBUF_COMPILER}
                COMMENT "Running C++ protocol buffer compiler on ${ABS_FIL}"
                VERBATIM)
    endforeach ()
    set_source_files_properties(${${SRCS}} ${${HDRS}} PROPERTIES GENERATED TRUE)
    set(${SRCS} ${${SRCS}} PARENT_SCOPE)
    set(${HDRS} ${${HDRS}} PARENT_SCOPE)
endfunction()

set(PROTOBUF_GENERATE_CPP_APPEND_PATH true)
