# VERSION: V1.1
# IDL_GENERATED_DIR: the path .h & .cxx generated
# IDL_PP_PATH: the import path
################################################################################
########################## define functions ####################################
function(_find_fastddsidl_compiler)
    set(FASTDDSIDL_COMPILER_CANDIDATES "${FastDDS_PREFIX}/bin/fastddsgen")
    foreach (candidate ${FASTDDSIDL_COMPILER_CANDIDATES})
        if (EXISTS ${candidate})
            set(FASTDDSIDL_COMPILER ${candidate} PARENT_SCOPE)
            return()
        endif ()
    endforeach ()
    message(FATAL_ERROR "FASTDDSIDL_COMPILER_CANDIDATES:" ${FASTDDSIDL_COMPILER_CANDIDATES})
    message(FATAL_ERROR "Couldn't find fastddsgen  compiler. Please ensure that fastddsgen is properly installed to /usr/local from source. Checked the following paths: ${FASTDDSIDL_COMPILER_CANDIDATES}")
endfunction()

# ==================== FASTDDSILD_GENERATE_CXX  ==========================
function(FASTDDSIDL_GENERATE_CXX SRCS HDRS)
    if (NOT ARGN)
        message(SEND_ERROR "Error: FASTDDSILD_GENERATE_CXX called without any .idl files")
        return()
    endif ()
    if (FASTDDSILD_GENERATE_CXX_APPEND_PATH)
        # Create an include path for each file specified
        message(STATUS "FASTDDSILD_GENERATE_CXX: TRUE")
        foreach (FIL ${ARGN})
            get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
            get_filename_component(ABS_PATH ${ABS_FIL} PATH)
            list(FIND _idl_include_path ${ABS_PATH} _contains_already)
            if (${_contains_already} EQUAL -1)
                list(APPEND _idl_include_path -I ${ABS_PATH})
            endif ()
        endforeach ()
    else ()
        # assume all idl are in project_name/idl folder
        set(_idl -I ${CMAKE_CURRENT_SOURCE_DIR}/idl)
    endif ()

    list(APPEND _idl_include_path -I ${CMAKE_CURRENT_SOURCE_DIR})


    set(${SRCS})
    set(${HDRS})
    _find_fastddsidl_compiler()
    foreach (FIL ${ARGN})
        get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
        get_filename_component(FIL_WE ${FIL} NAME_WE)
        get_filename_component(RELT_DIR ${FIL} DIRECTORY)
        # generated the same directory structure for proto files
        set(GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}")

        message(STATUS "GENERATED_DIR:" ${GENERATED_DIR})

        list(APPEND GENERATED_SRC "${GENERATED_DIR}/${FIL_WE}.cxx")
        list(APPEND GENERATED_SRC "${GENERATED_DIR}/${FIL_WE}PubSubTypes.cxx")
        list(APPEND GENERATED_HDR "${GENERATED_DIR}/${FIL_WE}.h")
        list(APPEND GENERATED_HDR "${GENERATED_DIR}/${FIL_WE}PubSubTypes.h")

        list(APPEND ${SRCS} "${GENERATED_SRC}")
        list(APPEND ${HDRS} "${GENERATED_HDR}")

        execute_process(COMMAND -cs ${FASTDDSIDL_COMPILER} -I ${IDL_PP_PATH} -d ${IDL_GENERATED_DIR} -replace ${ABS_FIL})
    endforeach ()
    set_source_files_properties(${${SRCS}} ${${HDRS}} PROPERTIES GENERATED TRUE)
    set(${SRCS} ${${SRCS}} PARENT_SCOPE)
    set(${HDRS} ${${HDRS}} PARENT_SCOPE)


endfunction()

set(FASTDDSILD_GENERATE_CXX_APPEND_PATH true)
