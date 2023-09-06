
# [API](https://jinja.palletsprojects.com/en/3.1.x/api/#api "Permalink to this heading")

This document describes the API to Jinja and not the template language (for that, see [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)). It will be most useful as reference to those implementing the template interface to the application and not those who are creating Jinja templates.

## [Basics](https://jinja.palletsprojects.com/en/3.1.x/api/#basics "Permalink to this heading")

Jinja uses a central object called the template [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment"). Instances of this class are used to store the configuration and global objects, and are used to load templates from the file system or other locations. Even if you are creating templates from strings by using the constructor of [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template") class, an environment is created automatically for you, albeit a shared one.

Most applications will create one [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment") object on application initialization and use that to load templates. In some cases however, it’s useful to have multiple environments side by side, if different configurations are in use.

The simplest way to configure Jinja to load templates for your application is to use [`PackageLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.PackageLoader "jinja2.loaders.PackageLoader").

```python
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("yourapp"),
    autoescape=select_autoescape()
)```

This will create a template environment with a loader that looks up templates in the `templates` folder inside the `yourapp` Python package (or next to the `yourapp.py` Python module). It also enables autoescaping for HTML files. This loader only requires that `yourapp` is importable, it figures out the absolute path to the folder for you.

Different loaders are available to load templates in other ways or from other locations. They’re listed in the [Loaders](https://jinja.palletsprojects.com/en/3.1.x/api/#loaders) section below. You can also write your own if you want to load templates from a source that’s more specialized to your project.

To load a template from this environment, call the `get_template()` method, which returns the loaded [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template").

template = env.get_template("mytemplate.html")

To render it with some variables, call the `render()` method.

print(template.render(the="variables", go="here"))

Using a template loader rather than passing strings to [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template") or [`Environment.from_string()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.from_string "jinja2.Environment.from_string") has multiple advantages. Besides being a lot easier to use it also enables template inheritance.

Notes on Autoescaping

In future versions of Jinja we might enable autoescaping by default for security reasons. As such you are encouraged to explicitly configure autoescaping now instead of relying on the default.

## [High Level API](https://jinja.palletsprojects.com/en/3.1.x/api/#high-level-api "Permalink to this heading")

The high-level API is the API you will use in the application to load and render Jinja templates. The [Low Level API](https://jinja.palletsprojects.com/en/3.1.x/api/#low-level-api) on the other side is only useful if you want to dig deeper into Jinja or [develop extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja-extensions).

[_class_ jinja2.Environment([_options_])](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "Permalink to this definition")

The core component of Jinja is the Environment. It contains important shared variables like configuration, filters, tests, globals and others. Instances of this class may be modified if they are not shared and if no template was loaded so far. Modifications on environments after the first template was loaded will lead to surprising effects and undefined behavior.

Here are the possible initialization parameters:

> block_start_string
> 
> The string marking the beginning of a block. Defaults to `'{%'`.
> 
> block_end_string
> 
> The string marking the end of a block. Defaults to `'%}'`.
> 
> variable_start_string
> 
> The string marking the beginning of a print statement. Defaults to `'{{'`.
> 
> variable_end_string
> 
> The string marking the end of a print statement. Defaults to `'}}'`.
> 
> comment_start_string
> 
> The string marking the beginning of a comment. Defaults to `'{#'`.
> 
> comment_end_string
> 
> The string marking the end of a comment. Defaults to `'#}'`.
> 
> line_statement_prefix
> 
> If given and a string, this will be used as prefix for line based statements. See also [Line Statements](https://jinja.palletsprojects.com/en/3.1.x/templates/#line-statements).
> 
> line_comment_prefix
> 
> If given and a string, this will be used as prefix for line based comments. See also [Line Statements](https://jinja.palletsprojects.com/en/3.1.x/templates/#line-statements).
> 
> Changelog
> 
> trim_blocks
> 
> If this is set to `True` the first newline after a block is removed (block, not variable tag!). Defaults to False.
> 
> lstrip_blocks
> 
> If this is set to `True` leading spaces and tabs are stripped from the start of a line to a block. Defaults to False.
> 
> newline_sequence
> 
> The sequence that starts a newline. Must be one of `'\r'`, `'\n'` or `'\r\n'`. The default is `'\n'` which is a useful default for Linux and OS X systems as well as web applications.
> 
> keep_trailing_newline
> 
> Preserve the trailing newline when rendering templates. The default is `False`, which causes a single newline, if present, to be stripped from the end of the template.
> 
> Changelog
> 
> extensions
> 
> List of Jinja extensions to use. This can either be import paths as strings or extension classes. For more information have a look at [the extensions documentation](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja-extensions).
> 
> optimized
> 
> should the optimizer be enabled? Default is `True`.
> 
> undefined
> 
> [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") or a subclass of it that is used to represent undefined values in the template.
> 
> finalize
> 
> A callable that can be used to process the result of a variable expression before it is output. For example one can convert `None` implicitly into an empty string here.
> 
> autoescape
> 
> If set to `True` the XML/HTML autoescaping feature is enabled by default. For more details about autoescaping see `Markup`. As of Jinja 2.4 this can also be a callable that is passed the template name and has to return `True` or `False` depending on autoescape should be enabled by default.
> 
> Changelog
> 
> loader
> 
> The template loader for this environment.
> 
> cache_size
> 
> The size of the cache. Per default this is `400` which means that if more than 400 templates are loaded the loader will clean out the least recently used template. If the cache size is set to `0` templates are recompiled all the time, if the cache size is `-1` the cache will not be cleaned.
> 
> Changelog
> 
> auto_reload
> 
> Some loaders load templates from locations where the template sources may change (ie: file system or database). If `auto_reload` is set to `True` (default) every time a template is requested the loader checks if the source changed and if yes, it will reload the template. For higher performance it’s possible to disable that.
> 
> bytecode_cache
> 
> If set to a bytecode cache object, this object will provide a cache for the internal Jinja bytecode so that templates don’t have to be parsed if they were not changed.
> 
> See [Bytecode Cache](https://jinja.palletsprojects.com/en/3.1.x/api/#bytecode-cache) for more information.
> 
> enable_async
> 
> If set to true this enables async template execution which allows using async functions and generators.

Parameters:

- **block_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **block_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **line_statement_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **line_comment_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **trim_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **lstrip_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **newline_sequence** (_te.Literal__[__'\n'__,_ _'\r\n'__,_ _'\r'__]_) –
    
- **keep_trailing_newline** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **extensions** ([_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Extension_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.ext.Extension "jinja2.ext.Extension")_]__]_) –
    
- **optimized** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **undefined** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")_]_) –
    
- **finalize** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[__...__]__,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    
- **autoescape** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") _|_ [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None__]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_) –
    
- **loader** ([_BaseLoader_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.BaseLoader") _|_ _None_) –
    
- **cache_size** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) –
    
- **auto_reload** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **bytecode_cache** ([_BytecodeCache_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache "jinja2.BytecodeCache") _|_ _None_) –
    
- **enable_async** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

shared[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.shared "Permalink to this definition")

If a template was created by using the [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template") constructor an environment is created automatically. These environments are created as shared environments which means that multiple templates may have the same anonymous environment. For all shared environments this attribute is True, else False.

sandboxed[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.sandboxed "Permalink to this definition")

If the environment is sandboxed this attribute is True. For the sandbox mode have a look at the documentation for the [`SandboxedEnvironment`](https://jinja.palletsprojects.com/en/3.1.x/sandbox/#jinja2.sandbox.SandboxedEnvironment "jinja2.sandbox.SandboxedEnvironment").

filters[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.filters "Permalink to this definition")

A dict of filters for this environment. As long as no template was loaded it’s safe to add new filters or remove old. For custom filters see [Custom Filters](https://jinja.palletsprojects.com/en/3.1.x/api/#writing-filters). For valid filter names have a look at [Notes on Identifiers](https://jinja.palletsprojects.com/en/3.1.x/api/#identifier-naming).

tests[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.tests "Permalink to this definition")

A dict of test functions for this environment. As long as no template was loaded it’s safe to modify this dict. For custom tests see [Custom Tests](https://jinja.palletsprojects.com/en/3.1.x/api/#writing-tests). For valid test names have a look at [Notes on Identifiers](https://jinja.palletsprojects.com/en/3.1.x/api/#identifier-naming).

globals[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "Permalink to this definition")

A dict of variables that are available in every template loaded by the environment. As long as no template was loaded it’s safe to modify this. For more details see [The Global Namespace](https://jinja.palletsprojects.com/en/3.1.x/api/#global-namespace). For valid object names see [Notes on Identifiers](https://jinja.palletsprojects.com/en/3.1.x/api/#identifier-naming).

policies[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.policies "Permalink to this definition")

A dictionary with [Policies](https://jinja.palletsprojects.com/en/3.1.x/api/#policies). These can be reconfigured to change the runtime behavior or certain template features. Usually these are security related.

code_generator_class[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.code_generator_class "Permalink to this definition")

The class used for code generation. This should not be changed in most cases, unless you need to modify the Python code a template compiles to.

context_class[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.context_class "Permalink to this definition")

The context used for templates. This should not be changed in most cases, unless you need to modify internals of how template variables are handled. For details, see [`Context`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context").

overlay([_options_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.overlay "Permalink to this definition")

Create a new overlay environment that shares all the data with the current environment except for cache and the overridden attributes. Extensions cannot be removed for an overlayed environment. An overlayed environment automatically gets all the extensions of the environment it is linked to plus optional extra extensions.

Creating overlays should happen after the initial environment was set up completely. Not all attributes are truly linked, some are just copied over so modifications on the original environment may not shine through.

Changed in version 3.1.2: Added the `newline_sequence`,, `keep_trailing_newline`, and `enable_async` parameters to match `__init__`.

Parameters:

- **block_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **block_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **line_statement_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **line_comment_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **trim_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **lstrip_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **newline_sequence** (_te.Literal__[__'\n'__,_ _'\r\n'__,_ _'\r'__]_) –
    
- **keep_trailing_newline** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **extensions** ([_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Extension_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.ext.Extension "jinja2.ext.Extension")_]__]_) –
    
- **optimized** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **undefined** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")_]_) –
    
- **finalize** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[__...__]__,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    
- **autoescape** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") _|_ [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None__]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_) –
    
- **loader** ([_BaseLoader_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.BaseLoader") _|_ _None_) –
    
- **cache_size** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) –
    
- **auto_reload** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **bytecode_cache** ([_BytecodeCache_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache "jinja2.BytecodeCache") _|_ _None_) –
    
- **enable_async** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

Return type:

[Environment](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")

undefined([_hint_, _obj_, _name_, _exc_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.undefined "Permalink to this definition")

Creates a new [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") object for name. This is useful for filters or functions that may return undefined objects for some operations. All parameters except of hint should be provided as keyword parameters for better readability. The hint is used as error message for the exception if provided, otherwise the error message will be generated from obj and name automatically. The exception provided as exc is raised if something with the generated undefined object is done that the undefined object does not allow. The default exception is [`UndefinedError`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError"). If a hint is provided the name may be omitted.

The most common way to create an undefined object is by providing a name only:

return environment.undefined(name='some_name')

This means that the name some_name is not defined. If the name was from an attribute of an object it makes sense to tell the undefined object the holder object to improve the error message:

if not hasattr(obj, 'attr'):
    return environment.undefined(obj=obj, name='attr')

For a more complex example you can provide a hint. For example the `first()` filter creates an undefined object that way:

return environment.undefined('no first item, sequence was empty')

If it the name or obj is known (for example because an attribute was accessed) it should be passed to the undefined object, even if a custom hint is provided. This gives undefined objects the possibility to enhance the error message.

add_extension(_extension_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.add_extension "Permalink to this definition")

Adds an extension after the environment was created.

Changelog

Parameters:

**extension** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Extension_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.ext.Extension "jinja2.ext.Extension")_]_) –

Return type:

None

compile_expression(_source_, _undefined_to_none=True_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.compile_expression "Permalink to this definition")

A handy helper method that returns a callable that accepts keyword arguments that appear as variables in the expression. If called it returns the result of the expression.

This is useful if applications want to use the same rules as Jinja in template “configuration files” or similar situations.

Example usage:

>>> env = Environment()
>>> expr = env.compile_expression('foo == 42')
>>> expr(foo=23)
False
>>> expr(foo=42)
True

Per default the return value is converted to None if the expression returns an undefined value. This can be changed by setting undefined_to_none to False.

>>> env.compile_expression('var')() is None
True
>>> env.compile_expression('var', undefined_to_none=False)()
Undefined

Changelog

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **undefined_to_none** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

Return type:

_TemplateExpression_

compile_templates(_target_, _extensions=None_, _filter_func=None_, _zip='deflated'_, _log_function=None_, _ignore_errors=True_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.compile_templates "Permalink to this definition")

Finds all the templates the loader can find, compiles them and stores them in target. If zip is None, instead of in a zipfile, the templates will be stored in a directory. By default a deflate zip algorithm is used. To switch to the stored algorithm, zip can be set to `'stored'`.

extensions and filter_func are passed to [`list_templates()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.list_templates "jinja2.Environment.list_templates"). Each template returned will be compiled to the target folder or zipfile.

By default template compilation errors are ignored. In case a log function is provided, errors are logged. If you want template syntax errors to abort the compilation you can set ignore_errors to False and you will get an exception on syntax errors.

Changelog

Parameters:

- **target** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_PathLike_](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.11)")) –
    
- **extensions** ([_Collection_](https://docs.python.org/3/library/typing.html#typing.Collection "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_ _|_ _None_) –
    
- **filter_func** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_ _|_ _None_) –
    
- **zip** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **log_function** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]__,_ _None__]_ _|_ _None_) –
    
- **ignore_errors** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

Return type:

None

extend(_**attributes_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.extend "Permalink to this definition")

Add the items to the instance of the environment if they do not exist yet. This is used by [extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/#writing-extensions) to register callbacks and configuration values without breaking inheritance.

Parameters:

**attributes** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –

Return type:

None

from_string(_source_, _globals=None_, _template_class=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.from_string "Permalink to this definition")

Load a template from a source string without using `loader`.

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template "jinja2.nodes.Template")) – Jinja source to compile into a template.
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) – Extend the environment [`globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") with these extra variables available for all renders of this template. If the template has already been loaded and cached, its globals are updated with any new items.
    
- **template_class** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")_]_ _|_ _None_) – Return an instance of this [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template") class.
    

Return type:

[_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")

get_or_select_template(_template_name_or_list_, _parent=None_, _globals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_or_select_template "Permalink to this definition")

Use [`select_template()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.select_template "jinja2.Environment.select_template") if an iterable of template names is given, or [`get_template()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template "jinja2.Environment.get_template") if one name is given.

Changelog

Parameters:

- **template_name_or_list** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template") _|_ [_List_](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")_]_) –
    
- **parent** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    

Return type:

[_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")

get_template(_name_, _parent=None_, _globals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template "Permalink to this definition")

Load a template by name with `loader` and return a [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template"). If the template does not exist a [`TemplateNotFound`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateNotFound "jinja2.TemplateNotFound") exception is raised.

Parameters:

- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")) – Name of the template to load. When loading templates from the filesystem, “/” is used as the path separator, even on Windows.
    
- **parent** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) – The name of the parent template importing this template. [`join_path()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.join_path "jinja2.Environment.join_path") can be used to implement name transformations with this.
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) – Extend the environment [`globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") with these extra variables available for all renders of this template. If the template has already been loaded and cached, its globals are updated with any new items.
    

Return type:

[_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")

Changelog

[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template")

join_path(_template_, _parent_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.join_path "Permalink to this definition")

Join a template with the parent. By default all the lookups are relative to the loader root so this method returns the template parameter unchanged, but if the paths should be relative to the parent template, this function can be used to calculate the real template name.

Subclasses may override this method and implement template path joining here.

Parameters:

- **template** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **parent** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    

Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")

list_templates(_extensions=None_, _filter_func=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.list_templates "Permalink to this definition")

Returns a list of templates for this environment. This requires that the loader supports the loader’s `list_templates()` method.

If there are other files in the template folder besides the actual templates, the returned list can be filtered. There are two ways: either extensions is set to a list of file extensions for templates, or a filter_func can be provided which is a callable that is passed a template name and should return True if it should end up in the result list.

If the loader does not support that, a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.11)") is raised.

Changelog

Parameters:

- **extensions** ([_Collection_](https://docs.python.org/3/library/typing.html#typing.Collection "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_ _|_ _None_) –
    
- **filter_func** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_ _|_ _None_) –
    

Return type:

[_List_](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")]

select_template(_names_, _parent=None_, _globals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.select_template "Permalink to this definition")

Like [`get_template()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template "jinja2.Environment.get_template"), but tries loading multiple names. If none of the names can be loaded a [`TemplatesNotFound`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplatesNotFound "jinja2.TemplatesNotFound") exception is raised.

Parameters:

- **names** ([_Iterable_](https://docs.python.org/3/library/typing.html#typing.Iterable "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")_]_) – List of template names to try loading in order.
    
- **parent** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) – The name of the parent template importing this template. [`join_path()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.join_path "jinja2.Environment.join_path") can be used to implement name transformations with this.
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) – Extend the environment [`globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") with these extra variables available for all renders of this template. If the template has already been loaded and cached, its globals are updated with any new items.
    

Return type:

[_Template_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.environment.Template")

Changelog

[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined")[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError")[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined")

[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template")

_class_ jinja2.Template(_source_, _block_start_string='{%'_, _block_end_string='%}'_, _variable_start_string='{{'_, _variable_end_string='}}'_, _comment_start_string='{#'_, _comment_end_string='#}'_, _line_statement_prefix=None_, _line_comment_prefix=None_, _trim_blocks=False_, _lstrip_blocks=False_, _newline_sequence='\n'_, _keep_trailing_newline=False_, _extensions=()_, _optimized=True_, _undefined=<class 'jinja2.runtime.Undefined'>_, _finalize=None_, _autoescape=False_, _enable_async=False_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "Permalink to this definition")

A compiled template that can be rendered.

Use the methods on [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment") to create or load templates. The environment is used to configure how templates are compiled and behave.

It is also possible to create a template object directly. This is not usually recommended. The constructor takes most of the same arguments as [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment"). All templates created with the same environment arguments share the same ephemeral `Environment` instance behind the scenes.

A template object should be considered immutable. Modifications on the object are not supported.

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Template_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template "jinja2.nodes.Template")) –
    
- **block_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **block_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **variable_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_start_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **comment_end_string** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **line_statement_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **line_comment_prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **trim_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **lstrip_blocks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **newline_sequence** (_te.Literal__[__'\n'__,_ _'\r\n'__,_ _'\r'__]_) –
    
- **keep_trailing_newline** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **extensions** ([_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Extension_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.ext.Extension "jinja2.ext.Extension")_]__]_) –
    
- **optimized** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **undefined** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")_]_) –
    
- **finalize** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[__...__]__,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    
- **autoescape** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") _|_ [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None__]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_) –
    
- **enable_async** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

Return type:

[_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

globals[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.globals "Permalink to this definition")

A dict of variables that are available every time the template is rendered, without needing to pass them during render. This should not be modified, as depending on how the template was loaded it may be shared with the environment and other templates.

Defaults to [`Environment.globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") unless extra values are passed to [`Environment.get_template()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template "jinja2.Environment.get_template").

Globals are only intended for data that is common to every render of the template. Specific data should be passed to [`render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render").

See [The Global Namespace](https://jinja.palletsprojects.com/en/3.1.x/api/#global-namespace).

name[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.name "Permalink to this definition")

The loading name of the template. If the template was loaded from a string this is None.

filename[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.filename "Permalink to this definition")

The filename of the template on the file system if it was loaded from there. Otherwise this is None.

render([_context_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "Permalink to this definition")

This method accepts the same arguments as the dict constructor: A dict, a dict subclass or some keyword arguments. If no arguments are given the context will be empty. These two calls do the same:

template.render(knights='that say nih')
template.render({'knights': 'that say nih'})

This will return the rendered template as a string.

Parameters:

- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")

generate([_context_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.generate "Permalink to this definition")

For very large templates it can be useful to not render the whole template at once but evaluate each statement after another and yield piece for piece. This method basically does exactly that and returns a generator that yields one item after another as strings.

It accepts the same arguments as [`render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render").

Parameters:

- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[_Iterator_](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")]

stream([_context_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.stream "Permalink to this definition")

Works exactly like [`generate()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.generate "jinja2.Template.generate") but returns a `TemplateStream`.

Parameters:

- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[_TemplateStream_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.environment.TemplateStream "jinja2.environment.TemplateStream")

_async_ render_async([_context_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render_async "Permalink to this definition")

This works similar to [`render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render") but returns a coroutine that when awaited returns the entire rendered template string. This requires the async feature to be enabled.

Example usage:

await template.render_async(knights='that say nih; asynchronously')

Parameters:

- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")

_async_ generate_async([_context_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.generate_async "Permalink to this definition")

An async version of [`generate()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.generate "jinja2.Template.generate"). Works very similarly but returns an async iterator instead.

Parameters:

- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[_AsyncIterator_](https://docs.python.org/3/library/typing.html#typing.AsyncIterator "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")]

make_module(_vars=None_, _shared=False_, _locals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.make_module "Permalink to this definition")

This method works like the [`module`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.module "jinja2.Template.module") attribute when called without arguments but it will evaluate the template on every call rather than caching it. It’s also possible to provide a dict which is then used as context. The arguments are the same as for the [`new_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.new_context "jinja2.Template.new_context") method.

Parameters:

- **vars** ([_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    
- **shared** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **locals** ([_Mapping_](https://docs.python.org/3/library/typing.html#typing.Mapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    

Return type:

_TemplateModule_

_property_ module_: TemplateModule_[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.module "Permalink to this definition")

The template as module. This is used for imports in the template runtime but is also useful if one wants to access exported template variables from the Python layer:

>>> t = Template('{% macro foo() %}42{% endmacro %}23')
>>> str(t.module)
'23'
>>> t.module.foo() == u'42'
True

This attribute is not available if async mode is enabled.

_class_ jinja2.environment.TemplateStream[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.environment.TemplateStream "Permalink to this definition")

A template stream works pretty much like an ordinary python generator but it can buffer multiple items to reduce the number of total iterations. Per default the output is unbuffered which means that for every unbuffered instruction in the template one string is yielded.

If buffering is enabled with a buffer size of 5, five items are combined into a new string. This is mainly useful if you are streaming big templates to a client via WSGI which flushes after each iteration.

Parameters:

**gen** ([_Iterator_](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_) –

disable_buffering()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.environment.TemplateStream.disable_buffering "Permalink to this definition")

Disable the output buffering.

Return type:

None

dump(_fp_, _encoding=None_, _errors='strict'_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.environment.TemplateStream.dump "Permalink to this definition")

Dump the complete stream into a file or file-like object. Per default strings are written, if you want to encode before writing specify an encoding.

Example usage:

Template('Hello {{ name }}!').stream(name='foo').dump('hello.html')

Parameters:

- **fp** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_IO_](https://docs.python.org/3/library/typing.html#typing.IO "(in Python v3.11)")) –
    
- **encoding** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **errors** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

None

enable_buffering(_size=5_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.environment.TemplateStream.enable_buffering "Permalink to this definition")

Enable buffering. Buffer size items before yielding them.

Parameters:

**size** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) –

Return type:

None

## Autoescaping[](https://jinja.palletsprojects.com/en/3.1.x/api/#autoescaping "Permalink to this heading")

Changelog

Jinja now comes with autoescaping support. As of Jinja 2.9 the autoescape extension is removed and built-in. However autoescaping is not yet enabled by default though this will most likely change in the future. It’s recommended to configure a sensible default for autoescaping. This makes it possible to enable and disable autoescaping on a per-template basis (HTML versus text for instance).

jinja2.select_autoescape(_enabled_extensions=('html', 'htm', 'xml')_, _disabled_extensions=()_, _default_for_string=True_, _default=False_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.select_autoescape "Permalink to this definition")

Intelligently sets the initial value of autoescaping based on the filename of the template. This is the recommended way to configure autoescaping if you do not want to write a custom function yourself.

If you want to enable it for all templates created from strings or for all templates with .html and .xml extensions:

from jinja2 import Environment, select_autoescape
env = Environment(autoescape=select_autoescape(
    enabled_extensions=('html', 'xml'),
    default_for_string=True,
))

Example configuration to turn it on at all times except if the template ends with .txt:

from jinja2 import Environment, select_autoescape
env = Environment(autoescape=select_autoescape(
    disabled_extensions=('txt',),
    default_for_string=True,
    default=True,
))

The enabled_extensions is an iterable of all the extensions that autoescaping should be enabled for. Likewise disabled_extensions is a list of all templates it should be disabled for. If a template is loaded from a string then the default from default_for_string is used. If nothing matches then the initial value of autoescaping is set to the value of default.

For security reasons this function operates case insensitive.

Changelog

Parameters:

- **enabled_extensions** ([_Collection_](https://docs.python.org/3/library/typing.html#typing.Collection "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_) –
    
- **disabled_extensions** ([_Collection_](https://docs.python.org/3/library/typing.html#typing.Collection "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_) –
    
- **default_for_string** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **default** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

Return type:

[_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")[[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") | None], [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")]

Here a recommended setup that enables autoescaping for templates ending in `'.html'`, `'.htm'` and `'.xml'` and disabling it by default for all other extensions. You can use the [`select_autoescape()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.select_autoescape "jinja2.select_autoescape") function for this:

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(autoescape=select_autoescape(['html', 'htm', 'xml']),
                  loader=PackageLoader('mypackage'))

The `select_autoescape()` function returns a function that works roughly like this:

def autoescape(template_name):
    if template_name is None:
        return False
    if template_name.endswith(('.html', '.htm', '.xml'))

When implementing a guessing autoescape function, make sure you also accept None as valid template name. This will be passed when generating templates from strings. You should always configure autoescaping as defaults in the future might change.

Inside the templates the behaviour can be temporarily changed by using the autoescape block (see [Autoescape Overrides](https://jinja.palletsprojects.com/en/3.1.x/templates/#autoescape-overrides)).

## Notes on Identifiers[](https://jinja.palletsprojects.com/en/3.1.x/api/#notes-on-identifiers "Permalink to this heading")

Jinja uses Python naming rules. Valid identifiers can be any combination of characters accepted by Python.

Filters and tests are looked up in separate namespaces and have slightly modified identifier syntax. Filters and tests may contain dots to group filters and tests by topic. For example it’s perfectly valid to add a function into the filter dict and call it to.str. The regular expression for filter and test identifiers is `[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*`.

## Undefined Types[](https://jinja.palletsprojects.com/en/3.1.x/api/#undefined-types "Permalink to this heading")

These classes can be used as undefined types. The [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment") constructor takes an undefined parameter that can be one of those classes or a custom subclass of [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined"). Whenever the template engine is unable to look up a name or access an attribute one of those objects is created and returned. Some operations on undefined values are then allowed, others fail.

The closest to regular Python behavior is the [`StrictUndefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.StrictUndefined "jinja2.StrictUndefined") which disallows all operations beside testing if it’s an undefined object.

_class_ jinja2.Undefined[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "Permalink to this definition")

The default undefined type. This undefined type can be printed and iterated over, but every other access will raise an [`UndefinedError`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError"):

>>> foo = Undefined(name='foo')
>>> str(foo)
''
>>> not foo
True
>>> foo + 42
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined

Parameters:

- **hint** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **obj** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **exc** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_TemplateRuntimeError_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateRuntimeError "jinja2.exceptions.TemplateRuntimeError")_]_) –
    

_undefined_hint[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_hint "Permalink to this definition")

Either None or a string with the error message for the undefined object.

_undefined_obj[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_obj "Permalink to this definition")

Either None or the owner object that caused the undefined object to be created (for example because an attribute does not exist).

_undefined_name[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_name "Permalink to this definition")

The name for the undefined variable / attribute or just None if no such information exists.

_undefined_exception[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_exception "Permalink to this definition")

The exception that the undefined object wants to raise. This is usually one of [`UndefinedError`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError") or `SecurityError`.

_fail_with_undefined_error(_\*args_, _\**kwargs_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._fail_with_undefined_error "Permalink to this definition")

When called with any arguments this method raises [`_undefined_exception`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_exception "jinja2.Undefined._undefined_exception") with an error message generated from the undefined hints stored on the undefined object.

_class_ jinja2.ChainableUndefined[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.ChainableUndefined "Permalink to this definition")

An undefined that is chainable, where both `__getattr__` and `__getitem__` return itself rather than raising an [`UndefinedError`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError").

>>> foo = ChainableUndefined(name='foo')
>>> str(foo.bar['baz'])
''
>>> foo.bar['baz'] + 42
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined

Changelog

Parameters:

- **hint** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **obj** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **exc** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_TemplateRuntimeError_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateRuntimeError "jinja2.exceptions.TemplateRuntimeError")_]_) –
    

_class_ jinja2.DebugUndefined[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.DebugUndefined "Permalink to this definition")

An undefined that returns the debug info when printed.

>>> foo = DebugUndefined(name='foo')
>>> str(foo)
'{{ foo }}'
>>> not foo
True
>>> foo + 42
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined

Parameters:

- **hint** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **obj** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **exc** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_TemplateRuntimeError_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateRuntimeError "jinja2.exceptions.TemplateRuntimeError")_]_) –
    

_class_ jinja2.StrictUndefined[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.StrictUndefined "Permalink to this definition")

An undefined that barks on print and iteration as well as boolean tests and all kinds of comparisons. In other words: you can do nothing with it except checking if it’s defined using the defined test.

>>> foo = StrictUndefined(name='foo')
>>> str(foo)
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined
>>> not foo
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined
>>> foo + 42
Traceback (most recent call last):
  ...
jinja2.exceptions.UndefinedError: 'foo' is undefined

Parameters:

- **hint** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **obj** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **exc** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_TemplateRuntimeError_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateRuntimeError "jinja2.exceptions.TemplateRuntimeError")_]_) –
    

There is also a factory function that can decorate undefined objects to implement logging on failures:

jinja2.make_logging_undefined(_logger=None_, _base=<class 'jinja2.runtime.Undefined'>_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.make_logging_undefined "Permalink to this definition")

Given a logger object this returns a new undefined class that will log certain failures. It will log iterations and printing. If no logger is given a default logger is created.

Example:

logger = logging.getLogger(__name__)
LoggingUndefined = make_logging_undefined(
    logger=logger,
    base=Undefined
)

Changelog

Parameters:

- **logger** ([_logging.Logger_](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.11)") _|_ _None_) – the logger to use. If not provided, a default logger is created.
    
- **base** ([_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")_[_[_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")_]_) – the base class to add logging functionality to. This defaults to [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined").
    

Return type:

[_Type_](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")[[_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")]

Undefined objects are created by calling `undefined`.

Implementation

[`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") is implemented by overriding the special `__underscore__` methods. For example the default [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") class implements `__str__` to returns an empty string, while `__int__` and others fail with an exception. To allow conversion to int by returning `0` you can implement your own subclass.

class NullUndefined(Undefined):
    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

To disallow a method, override it and raise [`_undefined_exception`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_exception "jinja2.Undefined._undefined_exception"). Because this is very common there is the helper method [`_fail_with_undefined_error()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._fail_with_undefined_error "jinja2.Undefined._fail_with_undefined_error") that raises the error with the correct information. Here’s a class that works like the regular [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") but fails on iteration:

class NonIterableUndefined(Undefined):
    def __iter__(self):
        self._fail_with_undefined_error()

## The Context[](https://jinja.palletsprojects.com/en/3.1.x/api/#the-context "Permalink to this heading")

_class_ jinja2.runtime.Context[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "Permalink to this definition")

The template context holds the variables of a template. It stores the values passed to the template and also the names the template exports. Creating instances is neither supported nor useful as it’s created automatically at various stages of the template evaluation and should not be created by hand.

The context is immutable. Modifications on [`parent`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.parent "jinja2.runtime.Context.parent") **must not** happen and modifications on [`vars`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.vars "jinja2.runtime.Context.vars") are allowed from generated template code only. Template filters and global functions marked as `pass_context()` get the active context passed as first argument and are allowed to access the context read-only.

The template context supports read only dict operations (get, keys, values, items, iterkeys, itervalues, iteritems, __getitem__, __contains__). Additionally there is a [`resolve()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.resolve "jinja2.runtime.Context.resolve") method that doesn’t fail with a KeyError but returns an [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined") object for missing variables.

Parameters:

- **environment** ([_Environment_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")) –
    
- **parent** ([_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **blocks** ([_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_Context_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context")_]__,_ [_Iterator_](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]__]__]_) –
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    

parent[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.parent "Permalink to this definition")

A dict of read only, global variables the template looks up. These can either come from another [`Context`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context"), from the `Environment.globals` or `Template.globals` or points to a dict created by combining the globals with the variables passed to the render function. It must not be altered.

vars[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.vars "Permalink to this definition")

The template local variables. This list contains environment and context functions from the [`parent`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.parent "jinja2.runtime.Context.parent") scope as well as local modifications and exported variables from the template. The template will modify this dict during template evaluation but filters and context functions are not allowed to modify it.

environment[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.environment "Permalink to this definition")

The environment that loaded the template.

exported_vars[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.exported_vars "Permalink to this definition")

This set contains all the names the template exports. The values for the names are in the [`vars`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.vars "jinja2.runtime.Context.vars") dict. In order to get a copy of the exported variables as dict, [`get_exported()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.get_exported "jinja2.runtime.Context.get_exported") can be used.

name[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.name "Permalink to this definition")

The load name of the template owning this context.

blocks[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.blocks "Permalink to this definition")

A dict with the current mapping of blocks in the template. The keys in this dict are the names of the blocks, and the values a list of blocks registered. The last item in each list is the current active block (latest in the inheritance chain).

eval_ctx[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.eval_ctx "Permalink to this definition")

The current [Evaluation Context](https://jinja.palletsprojects.com/en/3.1.x/api/#eval-context).

call(_callable_, _\*args_, _\**kwargs_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.call "Permalink to this definition")

Call the callable with the arguments and keyword arguments provided but inject the active context or environment as first argument if the callable has `pass_context()` or `pass_environment()`.

Parameters:

- **_Context__obj** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")) –
    
- **args** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    
- **kwargs** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –
    

Return type:

[_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)") | [_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")

get(_key_, _default=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.get "Permalink to this definition")

Look up a variable by name, or return a default if the key is not found.

Parameters:

- **key** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The variable name to look up.
    
- **default** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)") _|_ _None_) – The value to return if the key is not found.
    

Return type:

[_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

get_all()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.get_all "Permalink to this definition")

Return the complete context as dict including the exported variables. For optimizations reasons this might not return an actual copy so be careful with using it.

Return type:

[_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")]

get_exported()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.get_exported "Permalink to this definition")

Get a new dict with the exported variables.

Return type:

[_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")]

resolve(_key_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.resolve "Permalink to this definition")

Look up a variable by name, or return an [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined") object if the key is not found.

If you need to add custom behavior, override [`resolve_or_missing()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.resolve_or_missing "jinja2.runtime.Context.resolve_or_missing"), not this method. The various lookup functions use that method, not this one.

Parameters:

**key** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The variable name to look up.

Return type:

[_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)") | [_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.runtime.Undefined")

resolve_or_missing(_key_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.resolve_or_missing "Permalink to this definition")

Look up a variable by name, or return a `missing` sentinel if the key is not found.

Override this method to add custom lookup behavior. [`resolve()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.resolve "jinja2.runtime.Context.resolve"), [`get()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context.get "jinja2.runtime.Context.get"), and `__getitem__()` use this method. Don’t call this method directly.

Parameters:

**key** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The variable name to look up.

Return type:

[_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

The context is immutable, it prevents modifications, and if it is modified somehow despite that those changes may not show up. For performance, Jinja does not use the context as data storage for, only as a primary data source. Variables that the template does not define are looked up in the context, but variables the template does define are stored locally.

Instead of modifying the context directly, a function should return a value that can be assigned to a variable within the template itself.

{% set comments = get_latest_comments() %}

## Loaders[](https://jinja.palletsprojects.com/en/3.1.x/api/#loaders "Permalink to this heading")

Loaders are responsible for loading templates from a resource such as the file system. The environment will keep the compiled modules in memory like Python’s sys.modules. Unlike sys.modules however this cache is limited in size by default and templates are automatically reloaded. All loaders are subclasses of [`BaseLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.BaseLoader"). If you want to create your own loader, subclass [`BaseLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.BaseLoader") and override get_source.

_class_ jinja2.BaseLoader[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "Permalink to this definition")

Baseclass for all loaders. Subclass this and override get_source to implement a custom loading mechanism. The environment provides a get_template method that calls the loader’s load method to get the [`Template`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template") object.

A very basic example for a loader that looks up templates on the file system could look like this:

from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime

class MyLoader(BaseLoader):

    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == getmtime(path)

get_source(_environment_, _template_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader.get_source "Permalink to this definition")

Get the template source, filename and reload helper for a template. It’s passed the environment and template name and has to return a tuple in the form `(source, filename, uptodate)` or raise a TemplateNotFound error if it can’t locate the template.

The source part of the returned tuple must be the source of the template as a string. The filename should be the name of the file on the filesystem if it was loaded from there, otherwise `None`. The filename is used by Python for the tracebacks if no loader extension is used.

The last item in the tuple is the uptodate function. If auto reloading is enabled it’s always called to check if the template changed. No arguments are passed so the function must store the old state somewhere (for example in a closure). If it returns False the template will be reloaded.

Parameters:

- **environment** ([_Environment_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")) –
    
- **template** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    

Return type:

[_Tuple_](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") | None, [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")[[], [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")] | None]

load(_environment_, _name_, _globals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader.load "Permalink to this definition")

Loads a template. This method looks up the template in the cache or loads one by calling [`get_source()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader.get_source "jinja2.BaseLoader.get_source"). Subclasses should not override this method as loaders working on collections of other loaders (such as [`PrefixLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.PrefixLoader "jinja2.PrefixLoader") or [`ChoiceLoader`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.ChoiceLoader "jinja2.ChoiceLoader")) will not call this method but get_source directly.

Parameters:

- **environment** ([_Environment_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **globals** ([_MutableMapping_](https://docs.python.org/3/library/typing.html#typing.MutableMapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    

Return type:

[Template](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template "jinja2.Template")

Here a list of the builtin loaders Jinja provides:

_class_ jinja2.FileSystemLoader(_searchpath_, _encoding='utf-8'_, _followlinks=False_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemLoader "Permalink to this definition")

Load templates from a directory in the file system.

The path can be relative or absolute. Relative paths are relative to the current working directory.

loader = FileSystemLoader("templates")

A list of paths can be given. The directories will be searched in order, stopping at the first matching template.

loader = FileSystemLoader(["/override/templates", "/default/templates"])

Parameters:

- **searchpath** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_PathLike_](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.11)") _|_ [_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_PathLike_](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.11)")_]_) – A path, or list of paths, to the directory that contains the templates.
    
- **encoding** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – Use this encoding to read the text from template files.
    
- **followlinks** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) – Follow symbolic links in the path.
    

Changelog

_class_ jinja2.PackageLoader(_package_name_, _package_path='templates'_, _encoding='utf-8'_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.PackageLoader "Permalink to this definition")

Load templates from a directory in a Python package.

Parameters:

- **package_name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – Import name of the package that contains the template directory.
    
- **package_path** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – Directory within the imported package that contains the templates.
    
- **encoding** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – Encoding of template files.
    

The following example looks up templates in the `pages` directory within the `project.ui` package.

loader = PackageLoader("project.ui", "pages")

Only packages installed as directories (standard pip behavior) or zip/egg files (less common) are supported. The Python API for introspecting data in packages is too limited to support other installation methods the way this loader requires.

There is limited support for [**PEP 420**](https://peps.python.org/pep-0420/) namespace packages. The template directory is assumed to only be in one namespace contributor. Zip files contributing to a namespace are not supported.

Changelog

_class_ jinja2.DictLoader(_mapping_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.DictLoader "Permalink to this definition")

Loads a template from a Python dict mapping template names to template source. This loader is useful for unittesting:

>>> loader = DictLoader({'index.html': 'source here'})

Because auto reloading is rarely useful this is disabled per default.

Parameters:

**mapping** ([_Mapping_](https://docs.python.org/3/library/typing.html#typing.Mapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]_) –

_class_ jinja2.FunctionLoader(_load_func_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FunctionLoader "Permalink to this definition")

A loader that is passed a function which does the loading. The function receives the name of the template and has to return either a string with the template source, a tuple in the form `(source, filename, uptodatefunc)` or None if the template does not exist.

>>> def load_template(name):
...     if name == 'index.html':
...         return '...'
...
>>> loader = FunctionLoader(load_template)

The uptodatefunc is a function that is called if autoreload is enabled and has to return True if the template is still up to date. For more details have a look at [`BaseLoader.get_source()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader.get_source "jinja2.BaseLoader.get_source") which has the same return value.

Parameters:

**load_func** ([_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_]__,_ [_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Tuple_](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None__,_ [_Callable_](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.11)")_[__[__]__,_ [_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_]_ _|_ _None__]_ _|_ _None__]_) –

_class_ jinja2.PrefixLoader(_mapping_, _delimiter='/'_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.PrefixLoader "Permalink to this definition")

A loader that is passed a dict of loaders where each loader is bound to a prefix. The prefix is delimited from the template by a slash per default, which can be changed by setting the delimiter argument to something else:

loader = PrefixLoader({
    'app1':     PackageLoader('mypackage.app1'),
    'app2':     PackageLoader('mypackage.app2')
})

By loading `'app1/index.html'` the file from the app1 package is loaded, by loading `'app2/index.html'` the file from the second.

Parameters:

- **mapping** ([_Mapping_](https://docs.python.org/3/library/typing.html#typing.Mapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_BaseLoader_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.loaders.BaseLoader")_]_) –
    
- **delimiter** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    

_class_ jinja2.ChoiceLoader(_loaders_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.ChoiceLoader "Permalink to this definition")

This loader works like the PrefixLoader just that no prefix is specified. If a template could not be found by one loader the next one is tried.

>>> loader = ChoiceLoader([
...     FileSystemLoader('/path/to/user/templates'),
...     FileSystemLoader('/path/to/system/templates')
... ])

This is useful if you want to allow users to override builtin templates from a different location.

Parameters:

**loaders** ([_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_BaseLoader_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader "jinja2.loaders.BaseLoader")_]_) –

_class_ jinja2.ModuleLoader(_path_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.ModuleLoader "Permalink to this definition")

This loader loads templates from precompiled templates.

Example usage:

>>> loader = ChoiceLoader([
...     ModuleLoader('/path/to/compiled/templates'),
...     FileSystemLoader('/path/to/templates')
... ])

Templates can be precompiled with [`Environment.compile_templates()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.compile_templates "jinja2.Environment.compile_templates").

Parameters:

**path** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_PathLike_](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.11)") _|_ [_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_PathLike_](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.11)")_]_) –

## Bytecode Cache[](https://jinja.palletsprojects.com/en/3.1.x/api/#bytecode-cache "Permalink to this heading")

Jinja 2.1 and higher support external bytecode caching. Bytecode caches make it possible to store the generated bytecode on the file system or a different location to avoid parsing the templates on first use.

This is especially useful if you have a web application that is initialized on the first request and Jinja compiles many templates at once which slows down the application.

To use a bytecode cache, instantiate it and pass it to the [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment").

_class_ jinja2.BytecodeCache[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache "Permalink to this definition")

To implement your own bytecode cache you have to subclass this class and override [`load_bytecode()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache.load_bytecode "jinja2.BytecodeCache.load_bytecode") and [`dump_bytecode()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache.dump_bytecode "jinja2.BytecodeCache.dump_bytecode"). Both of these methods are passed a [`Bucket`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket "jinja2.bccache.Bucket").

A very basic bytecode cache that saves the bytecode on the file system:

from os import path

class MyCache(BytecodeCache):

    def __init__(self, directory):
        self.directory = directory

    def load_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        if path.exists(filename):
            with open(filename, 'rb') as f:
                bucket.load_bytecode(f)

    def dump_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        with open(filename, 'wb') as f:
            bucket.write_bytecode(f)

A more advanced version of a filesystem based bytecode cache is part of Jinja.

clear()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache.clear "Permalink to this definition")

Clears the cache. This method is not used by Jinja but should be implemented to allow applications to clear the bytecode cache used by a particular environment.

Return type:

None

dump_bytecode(_bucket_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache.dump_bytecode "Permalink to this definition")

Subclasses have to override this method to write the bytecode from a bucket back to the cache. If it unable to do so it must not fail silently but raise an exception.

Parameters:

**bucket** ([_Bucket_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket "jinja2.bccache.Bucket")) –

Return type:

None

load_bytecode(_bucket_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BytecodeCache.load_bytecode "Permalink to this definition")

Subclasses have to override this method to load bytecode into a bucket. If they are not able to find code in the cache for the bucket, it must not do anything.

Parameters:

**bucket** ([_Bucket_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket "jinja2.bccache.Bucket")) –

Return type:

None

_class_ jinja2.bccache.Bucket(_environment_, _key_, _checksum_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket "Permalink to this definition")

Buckets are used to store the bytecode for one template. It’s created and initialized by the bytecode cache and passed to the loading functions.

The buckets get an internal checksum from the cache assigned and use this to automatically reject outdated cache material. Individual bytecode cache subclasses don’t have to care about cache invalidation.

Parameters:

- **environment** ([_Environment_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")) –
    
- **key** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **checksum** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    

environment[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.environment "Permalink to this definition")

The `Environment` that created the bucket.

key[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.key "Permalink to this definition")

The unique cache key for this bucket

code[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.code "Permalink to this definition")

The bytecode if it’s loaded, otherwise None.

bytecode_from_string(_string_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.bytecode_from_string "Permalink to this definition")

Load bytecode from bytes.

Parameters:

**string** ([_bytes_](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.11)")) –

Return type:

None

bytecode_to_string()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.bytecode_to_string "Permalink to this definition")

Return the bytecode as bytes.

Return type:

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.11)")

load_bytecode(_f_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.load_bytecode "Permalink to this definition")

Loads bytecode from a file or file like object.

Parameters:

**f** ([_BinaryIO_](https://docs.python.org/3/library/typing.html#typing.BinaryIO "(in Python v3.11)")) –

Return type:

None

reset()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.reset "Permalink to this definition")

Resets the bucket (unloads the bytecode).

Return type:

None

write_bytecode(_f_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.bccache.Bucket.write_bytecode "Permalink to this definition")

Dump the bytecode into the file or file like object passed.

Parameters:

**f** ([_IO_](https://docs.python.org/3/library/typing.html#typing.IO "(in Python v3.11)")_[_[_bytes_](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.11)")_]_) –

Return type:

None

Builtin bytecode caches:

_class_ jinja2.FileSystemBytecodeCache(_directory=None_, _pattern='__jinja2_%s.cache'_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.FileSystemBytecodeCache "Permalink to this definition")

A bytecode cache that stores bytecode on the filesystem. It accepts two arguments: The directory where the cache items are stored and a pattern string that is used to build the filename.

If no directory is specified a default cache directory is selected. On Windows the user’s temp directory is used, on UNIX systems a directory is created for the user in the system temp directory.

The pattern can be used to have multiple separate caches operate on the same directory. The default pattern is `'__jinja2_%s.cache'`. `%s` is replaced with the cache key.

>>> bcc = FileSystemBytecodeCache('/tmp/jinja_cache', '%s.cache')

This bytecode cache supports clearing of the cache using the clear method.

Parameters:

- **directory** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **pattern** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    

_class_ jinja2.MemcachedBytecodeCache(_client_, _prefix='jinja2/bytecode/'_, _timeout=None_, _ignore_memcache_errors=True_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.MemcachedBytecodeCache "Permalink to this definition")

This class implements a bytecode cache that uses a memcache cache for storing the information. It does not enforce a specific memcache library (tummy’s memcache or cmemcache) but will accept any class that provides the minimal interface required.

Libraries compatible with this class:

- [cachelib](https://github.com/pallets/cachelib)
    
- [python-memcached](https://pypi.org/project/python-memcached/)
    

(Unfortunately the django cache interface is not compatible because it does not support storing binary data, only text. You can however pass the underlying cache client to the bytecode cache which is available as django.core.cache.cache._client.)

The minimal interface for the client passed to the constructor is this:

Parameters:

- **client** (__MemcachedClient_) –
    
- **prefix** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **timeout** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") _|_ _None_) –
    
- **ignore_memcache_errors** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    

_class_ MinimalClientInterface[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.MemcachedBytecodeCache.MinimalClientInterface "Permalink to this definition")

set(_key_, _value_[, _timeout_])[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.MemcachedBytecodeCache.MinimalClientInterface.set "Permalink to this definition")

Stores the bytecode in the cache. value is a string and timeout the timeout of the key. If timeout is not provided a default timeout or no timeout should be assumed, if it’s provided it’s an integer with the number of seconds the cache item should exist.

get(_key_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.MemcachedBytecodeCache.MinimalClientInterface.get "Permalink to this definition")

Returns the value for the cache key. If the item does not exist in the cache the return value must be None.

The other arguments to the constructor are the prefix for all keys that is added before the actual cache key and the timeout for the bytecode in the cache system. We recommend a high (or no) timeout.

This bytecode cache does not support clearing of used items in the cache. The clear method is a no-operation function.

Changelog

## Async Support[](https://jinja.palletsprojects.com/en/3.1.x/api/#async-support "Permalink to this heading")

Changelog

Jinja supports the Python `async` and `await` syntax. For the template designer, this support (when enabled) is entirely transparent, templates continue to look exactly the same. However, developers should be aware of the implementation as it affects what types of APIs you can use.

By default, async support is disabled. Enabling it will cause the environment to compile different code behind the scenes in order to handle async and sync code in an asyncio event loop. This has the following implications:

- Template rendering requires an event loop to be available to the current thread. [`asyncio.get_running_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop "(in Python v3.11)") must return an event loop.
    
- The compiled code uses `await` for functions and attributes, and uses `async for` loops. In order to support using both async and sync functions in this context, a small wrapper is placed around all calls and access, which adds overhead compared to purely async code.
    
- Sync methods and filters become wrappers around their corresponding async implementations where needed. For example, `render` invokes `async_render`, and `|map` supports async iterables.
    

Awaitable objects can be returned from functions in templates and any function call in a template will automatically await the result. The `await` you would normally add in Python is implied. For example, you can provide a method that asynchronously loads data from a database, and from the template designer’s point of view it can be called like any other function.

## Policies[](https://jinja.palletsprojects.com/en/3.1.x/api/#policies "Permalink to this heading")

Starting with Jinja 2.9 policies can be configured on the environment which can slightly influence how filters and other template constructs behave. They can be configured with the [`policies`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.policies "jinja2.Environment.policies") attribute.

Example:

env.policies['urlize.rel'] = 'nofollow noopener'

`truncate.leeway`:

Configures the leeway default for the truncate filter. Leeway as introduced in 2.9 but to restore compatibility with older templates it can be configured to 0 to get the old behavior back. The default is 5.

`urlize.rel`:

A string that defines the items for the rel attribute of generated links with the urlize filter. These items are always added. The default is noopener.

`urlize.target`:

The default target that is issued for links from the urlize filter if no other target is defined by the call explicitly.

`urlize.extra_schemes`:

Recognize URLs that start with these schemes in addition to the default `http://`, `https://`, and `mailto:`.

`json.dumps_function`:

If this is set to a value other than None then the tojson filter will dump with this function instead of the default one. Note that this function should accept arbitrary extra arguments which might be passed in the future from the filter. Currently the only argument that might be passed is indent. The default dump function is `json.dumps`.

`json.dumps_kwargs`:

Keyword arguments to be passed to the dump function. The default is `{'sort_keys': True}`.

`ext.i18n.trimmed`:

If this is set to True, `{% trans %}` blocks of the [i18n Extension](https://jinja.palletsprojects.com/en/3.1.x/extensions/#i18n-extension) will always unify linebreaks and surrounding whitespace as if the trimmed modifier was used.

## Utilities[](https://jinja.palletsprojects.com/en/3.1.x/api/#utilities "Permalink to this heading")

These helper functions and classes are useful if you add custom filters or functions to a Jinja environment.

jinja2.pass_context(_f_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_context "Permalink to this definition")

Pass the [`Context`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context") as the first argument to the decorated function when called while rendering a template.

Can be used on functions, filters, and tests.

If only `Context.eval_context` is needed, use [`pass_eval_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_eval_context "jinja2.pass_eval_context"). If only `Context.environment` is needed, use [`pass_environment()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_environment "jinja2.pass_environment").

Changelog

Parameters:

**f** (_F_) –

Return type:

_F_

jinja2.pass_eval_context(_f_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_eval_context "Permalink to this definition")

Pass the [`EvalContext`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.nodes.EvalContext "jinja2.nodes.EvalContext") as the first argument to the decorated function when called while rendering a template. See [Evaluation Context](https://jinja.palletsprojects.com/en/3.1.x/api/#eval-context).

Can be used on functions, filters, and tests.

If only `EvalContext.environment` is needed, use [`pass_environment()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_environment "jinja2.pass_environment").

Changelog

Parameters:

**f** (_F_) –

Return type:

_F_

jinja2.pass_environment(_f_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_environment "Permalink to this definition")

Pass the [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment") as the first argument to the decorated function when called while rendering a template.

Can be used on functions, filters, and tests.

Changelog

Parameters:

**f** (_F_) –

Return type:

_F_

jinja2.clear_caches()[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.clear_caches "Permalink to this definition")

Jinja keeps internal caches for environments and lexers. These are used so that Jinja doesn’t have to recreate environments and lexers all the time. Normally you don’t have to care about that but if you are measuring memory consumption you may want to clean the caches.

Return type:

None

jinja2.is_undefined(_obj_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.is_undefined "Permalink to this definition")

Check if the object passed is undefined. This does nothing more than performing an instance check against [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") but looks nicer. This can be used for custom filters or tests that want to react to undefined variables. For example a custom default filter can look like this:

def default(var, default=''):
    if is_undefined(var):
        return default
    return var

Parameters:

**obj** ([_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")) –

Return type:

[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")

## Exceptions[](https://jinja.palletsprojects.com/en/3.1.x/api/#exceptions "Permalink to this heading")

_exception_ jinja2.TemplateError(_message=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateError "Permalink to this definition")

Baseclass for all template errors.

Parameters:

**message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –

Return type:

None

_exception_ jinja2.UndefinedError(_message=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "Permalink to this definition")

Raised if a template tries to operate on [`Undefined`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined").

Parameters:

**message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –

Return type:

None

_exception_ jinja2.TemplateNotFound(_name_, _message=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateNotFound "Permalink to this definition")

Raised if a template does not exist.

Changelog

[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined")[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.UndefinedError "jinja2.UndefinedError")

Parameters:

- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined") _|_ _None_) –
    
- **message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

None

_exception_ jinja2.TemplatesNotFound(_names=()_, _message=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplatesNotFound "Permalink to this definition")

Like [`TemplateNotFound`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateNotFound "jinja2.TemplateNotFound") but raised if multiple templates are selected. This is a subclass of [`TemplateNotFound`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateNotFound "jinja2.TemplateNotFound") exception, so just catching the base exception will catch both.

Changelog

[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined")

Parameters:

- **names** ([_Sequence_](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ [_Undefined_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined "jinja2.Undefined")_]_) –
    
- **message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

None

_exception_ jinja2.TemplateSyntaxError(_message_, _lineno_, _name=None_, _filename=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError "Permalink to this definition")

Raised to tell the user that there is a problem with the template.

Parameters:

- **message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **lineno** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

None

message[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError.message "Permalink to this definition")

The error message.

lineno[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError.lineno "Permalink to this definition")

The line number where the error occurred.

name[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError.name "Permalink to this definition")

The load name for the template.

filename[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError.filename "Permalink to this definition")

The filename that loaded the template in the encoding of the file system (most likely utf-8, or mbcs on Windows systems).

_exception_ jinja2.TemplateRuntimeError(_message=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateRuntimeError "Permalink to this definition")

A generic runtime error in the template engine. Under some situations Jinja may raise this exception.

Parameters:

**message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –

Return type:

None

_exception_ jinja2.TemplateAssertionError(_message_, _lineno_, _name=None_, _filename=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateAssertionError "Permalink to this definition")

Like a template syntax error, but covers cases where something in the template caused an error at compile time that wasn’t necessarily caused by a syntax error. However it’s a direct subclass of [`TemplateSyntaxError`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError "jinja2.TemplateSyntaxError") and has the same attributes.

Parameters:

- **message** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **lineno** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

None

## Custom Filters[](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters "Permalink to this heading")

Filters are Python functions that take the value to the left of the filter as the first argument and produce a new value. Arguments passed to the filter are passed after the value.

For example, the filter `{{ 42|myfilter(23) }}` is called behind the scenes as `myfilter(42, 23)`.

Jinja comes with some [built-in filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters). To use a custom filter, write a function that takes at least a `value` argument, then register it in [`Environment.filters`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.filters "jinja2.Environment.filters").

Here’s a filter that formats datetime objects:

def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

environment.filters["datetime_format"] = datetime_format

Now it can be used in templates:

{{ article.pub_date|datetimeformat }}
{{ article.pub_date|datetimeformat("%B %Y") }}

Some decorators are available to tell Jinja to pass extra information to the filter. The object is passed as the first argument, making the value being filtered the second argument.

- [`pass_environment()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_environment "jinja2.pass_environment") passes the [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment").
    
- [`pass_eval_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_eval_context "jinja2.pass_eval_context") passes the [Evaluation Context](https://jinja.palletsprojects.com/en/3.1.x/api/#eval-context).
    
- [`pass_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_context "jinja2.pass_context") passes the current [`Context`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context").
    

Here’s a filter that converts line breaks into HTML `<br>` and `<p>` tags. It uses the eval context to check if autoescape is currently enabled before escaping the input and marking the output safe.

import re
from jinja2 import pass_eval_context
from markupsafe import Markup, escape

@pass_eval_context
def nl2br(eval_ctx, value):
    br = "<br>\n"

    if eval_ctx.autoescape:
        value = escape(value)
        br = Markup(br)

    result = "\n\n".join(
        f"<p>{br.join(p.splitlines())}<\p>"
        for p in re.split(r"(?:\r\n|\r(?!\n)|\n){2,}", value)
    )
    return Markup(result) if autoescape else result

## Custom Tests[](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-tests "Permalink to this heading")

Test are Python functions that take the value to the left of the test as the first argument, and return `True` or `False`. Arguments passed to the test are passed after the value.

For example, the test `{{ 42 is even }}` is called behind the scenes as `is_even(42)`.

Jinja comes with some [built-in tests](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-tests). To use a custom tests, write a function that takes at least a `value` argument, then register it in [`Environment.tests`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.tests "jinja2.Environment.tests").

Here’s a test that checks if a value is a prime number:

import math

def is_prime(n):
    if n == 2:
        return True

    for i in range(2, int(math.ceil(math.sqrt(n))) + 1):
        if n % i == 0:
            return False

    return True

environment.tests["prime"] = is_prime

Now it can be used in templates:

{% if value is prime %}
    {{ value }} is a prime number
{% else %}
    {{ value }} is not a prime number
{% endif %}

Some decorators are available to tell Jinja to pass extra information to the test. The object is passed as the first argument, making the value being tested the second argument.

- [`pass_environment()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_environment "jinja2.pass_environment") passes the [`Environment`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment").
    
- [`pass_eval_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_eval_context "jinja2.pass_eval_context") passes the [Evaluation Context](https://jinja.palletsprojects.com/en/3.1.x/api/#eval-context).
    
- [`pass_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.pass_context "jinja2.pass_context") passes the current [`Context`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context").
    

## Evaluation Context[](https://jinja.palletsprojects.com/en/3.1.x/api/#evaluation-context "Permalink to this heading")

The evaluation context (short eval context or eval ctx) makes it possible to activate and deactivate compiled features at runtime.

Currently it is only used to enable and disable automatic escaping, but it can be used by extensions as well.

The `autoescape` setting should be checked on the evaluation context, not the environment. The evaluation context will have the computed value for the current template.

Instead of `pass_environment`:

@pass_environment
def filter(env, value):
    result = do_something(value)

    if env.autoescape:
        result = Markup(result)

    return result

Use `pass_eval_context` if you only need the setting:

@pass_eval_context
def filter(eval_ctx, value):
    result = do_something(value)

    if eval_ctx.autoescape:
        result = Markup(result)

    return result

Or use `pass_context` if you need other context behavior as well:

@pass_context
def filter(context, value):
    result = do_something(value)

    if context.eval_ctx.autoescape:
        result = Markup(result)

    return result

The evaluation context must not be modified at runtime. Modifications must only happen with a [`nodes.EvalContextModifier`](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.EvalContextModifier "jinja2.nodes.EvalContextModifier") and [`nodes.ScopedEvalContextModifier`](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.ScopedEvalContextModifier "jinja2.nodes.ScopedEvalContextModifier") from an extension, not on the eval context object itself.

_class_ jinja2.nodes.EvalContext(_environment_, _template_name=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.nodes.EvalContext "Permalink to this definition")

Holds evaluation time information. Custom attributes can be attached to it in extensions.

Parameters:

- **environment** ([_Environment_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment "jinja2.Environment")) –
    
- **template_name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

autoescape[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.nodes.EvalContext.autoescape "Permalink to this definition")

True or False depending on if autoescaping is active or not.

volatile[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.nodes.EvalContext.volatile "Permalink to this definition")

True if the compiler cannot evaluate some expressions at compile time. At runtime this should always be False.

## The Global Namespace[](https://jinja.palletsprojects.com/en/3.1.x/api/#the-global-namespace "Permalink to this heading")

The global namespace stores variables and functions that should be available without needing to pass them to [`Template.render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render"). They are also available to templates that are imported or included without context. Most applications should only use [`Environment.globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals").

[`Environment.globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") are intended for data that is common to all templates loaded by that environment. [`Template.globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.globals "jinja2.Template.globals") are intended for data that is common to all renders of that template, and default to [`Environment.globals`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals "jinja2.Environment.globals") unless they’re given in [`Environment.get_template()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template "jinja2.Environment.get_template"), etc. Data that is specific to a render should be passed as context to [`Template.render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render").

Only one set of globals is used during any specific rendering. If templates A and B both have template globals, and B extends A, then only B’s globals are used for both when using `b.render()`.

Environment globals should not be changed after loading any templates, and template globals should not be changed at any time after loading the template. Changing globals after loading a template will result in unexpected behavior as they may be shared between the environment and other templates.

## Low Level API[](https://jinja.palletsprojects.com/en/3.1.x/api/#low-level-api "Permalink to this heading")

The low level API exposes functionality that can be useful to understand some implementation details, debugging purposes or advanced [extension](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja-extensions) techniques. Unless you know exactly what you are doing we don’t recommend using any of those.

Environment.lex(_source_, _name=None_, _filename=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.lex "Permalink to this definition")

Lex the given sourcecode and return a generator that yields tokens as tuples in the form `(lineno, token_type, value)`. This can be useful for [extension development](https://jinja.palletsprojects.com/en/3.1.x/extensions/#writing-extensions) and debugging templates.

This does not perform preprocessing. If you want the preprocessing of the extensions to be applied you have to filter source through the [`preprocess()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.preprocess "jinja2.Environment.preprocess") method.

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

[_Iterator_](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")[[_Tuple_](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.11)")[[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")]]

Environment.parse(_source_, _name=None_, _filename=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.parse "Permalink to this definition")

Parse the sourcecode and return the abstract syntax tree. This tree of nodes is used by the compiler to convert the template into executable source- or bytecode. This is useful for debugging or to extract information from templates.

If you are [developing Jinja extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/#writing-extensions) this gives you a good overview of the node tree generated.

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

[_Template_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template "jinja2.nodes.Template")

Environment.preprocess(_source_, _name=None_, _filename=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.preprocess "Permalink to this definition")

Preprocesses the source with all extensions. This is automatically called for all parsing and compiling methods but _not_ for [`lex()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.lex "jinja2.Environment.lex") because there you usually only want the actual source tokenized.

Parameters:

- **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) –
    
- **name** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    
- **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") _|_ _None_) –
    

Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")

Template.new_context(_vars=None_, _shared=False_, _locals=None_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.new_context "Permalink to this definition")

Create a new `Context` for this template. The vars provided will be passed to the template. Per default the globals are added to the context. If shared is set to True the data is passed as is to the context without adding the globals.

locals can be a dict of local variables for internal usage.

Parameters:

- **vars** ([_Dict_](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    
- **shared** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")) –
    
- **locals** ([_Mapping_](https://docs.python.org/3/library/typing.html#typing.Mapping "(in Python v3.11)")_[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_,_ [_Any_](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_]_ _|_ _None_) –
    

Return type:

[_Context_](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.runtime.Context "jinja2.runtime.Context")

Template.root_render_func(_context_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.root_render_func "Permalink to this definition")

This is the low level render function. It’s passed a `Context` that has to be created by [`new_context()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.new_context "jinja2.Template.new_context") of the same template or a compatible template. This render function is generated by the compiler from the template code and returns a generator that yields strings.

If an exception in the template code happens the template engine will not rewrite the exception but pass through the original one. As a matter of fact this function should only be called from within a [`render()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render "jinja2.Template.render") / [`generate()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.generate "jinja2.Template.generate") / [`stream()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.stream "jinja2.Template.stream") call.

Template.blocks[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.blocks "Permalink to this definition")

A dict of block render functions. Each of these functions works exactly like the [`root_render_func()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.root_render_func "jinja2.Template.root_render_func") with the same limitations.

Template.is_up_to_date[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.is_up_to_date "Permalink to this definition")

This attribute is False if there is a newer version of the template available, otherwise True.

Note

The low-level API is fragile. Future Jinja versions will try not to change it in a backwards incompatible way but modifications in the Jinja core may shine through. For example if Jinja introduces a new AST node in later versions that may be returned by [`parse()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.parse "jinja2.Environment.parse").

## The Meta API[](https://jinja.palletsprojects.com/en/3.1.x/api/#the-meta-api "Permalink to this heading")

Changelog

The meta API returns some information about abstract syntax trees that could help applications to implement more advanced template concepts. All the functions of the meta API operate on an abstract syntax tree as returned by the [`Environment.parse()`](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.parse "jinja2.Environment.parse") method.

jinja2.meta.find_undeclared_variables(_ast_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.meta.find_undeclared_variables "Permalink to this definition")

Returns a set of all variables in the AST that will be looked up from the context at runtime. Because at compile time it’s not known which variables will be used depending on the path the execution takes at runtime, all variables are returned.

>>> from jinja2 import Environment, meta
>>> env = Environment()
>>> ast = env.parse('{% set foo = 42 %}{{ bar + foo }}')
>>> meta.find_undeclared_variables(ast) == {'bar'}
True

Implementation

Internally the code generator is used for finding undeclared variables. This is good to know because the code generator might raise a `TemplateAssertionError` during compilation and as a matter of fact this function can currently raise that exception as well.

Parameters:

**ast** ([_Template_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template "jinja2.nodes.Template")) –

Return type:

[_Set_](https://docs.python.org/3/library/typing.html#typing.Set "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")]

jinja2.meta.find_referenced_templates(_ast_)[](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.meta.find_referenced_templates "Permalink to this definition")

Finds all the referenced templates from the AST. This will return an iterator over all the hardcoded template extensions, inclusions and imports. If dynamic inheritance or inclusion is used, None will be yielded.

>>> from jinja2 import Environment, meta
>>> env = Environment()
>>> ast = env.parse('{% extends "layout.html" %}{% include helper %}')
>>> list(meta.find_referenced_templates(ast))
['layout.html', None]

This function is useful for dependency tracking. For example if you want to rebuild parts of the website after a layout template has changed.

Parameters:

**ast** ([_Template_](https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template "jinja2.nodes.Template")) –

Return type:

[_Iterator_](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") | None]